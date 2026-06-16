"""
HITL Lab — AI Adapter Base
Portabilidad multi-nube + controles ISO 27001 / 42001 / 22301
"""

import os
import json
import time
import hashlib
from datetime import datetime, timezone
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

log = structlog.get_logger()

# ── ISO 42001: registro de versión del modelo usado ───────
MODEL_REGISTRY = {
    "claude":   "claude-sonnet-4-6",
    "watsonx":  "ibm/granite-13b-chat-v2",
    "bedrock":  os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
    "gemini":   os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
    "openai":   "gpt-4o",
}

# ── ISO 22301: respuesta de fallback si todos fallan ──────
FALLBACK_RESPONSE = (
    "[HITL-DRP] Servicio AI temporalmente no disponible. "
    "RTO estimado: 4 horas. Contacta soporte@hitl.mx"
)


class AIAdapter:
    """
    Adapter multi-nube para HITL Lab.

    ISO 27001: secrets solo desde variables de entorno.
    ISO 42001: cada llamada queda registrada en audit log.
    ISO 22301: fallback automático si el proveedor falla.
    """

    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or os.getenv("PROVIDER", "claude")
        self.model = MODEL_REGISTRY.get(self.provider, "unknown")
        self.audit_enabled = os.getenv("AUDIT_LOG_ENABLED", "true") == "true"
        self.audit_path = os.getenv("AUDIT_LOG_PATH", "/home/jovyan/data/audit.jsonl")

    # ── Método principal ──────────────────────────────────
    def complete(self, prompt: str, system: str = "") -> str:
        """
        Envía un prompt al proveedor activo.
        Cambia de proveedor cambiando PROVIDER en .env
        """
        start = time.time()
        response = FALLBACK_RESPONSE  # default ISO 22301

        try:
            if self.provider == "claude":
                response = self._call_claude(prompt, system)
            elif self.provider == "watsonx":
                response = self._call_watsonx(prompt, system)
            elif self.provider == "bedrock":
                response = self._call_bedrock(prompt, system)
            elif self.provider == "gemini":
                response = self._call_gemini(prompt, system)
            elif self.provider == "openai":
                response = self._call_openai(prompt, system)
            else:
                log.warning("proveedor_desconocido", provider=self.provider)

        except Exception as e:
            log.error("ai_call_failed", provider=self.provider, error=str(e))
            response = FALLBACK_RESPONSE  # ISO 22301

        finally:
            latency = round(time.time() - start, 3)
            self._audit_log(prompt, response, latency)  # ISO 42001

        return response

    # ── Anthropic / Claude ────────────────────────────────
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def _call_claude(self, prompt: str, system: str) -> str:
        import anthropic
        client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")  # ISO 27001: nunca hardcoded
        )
        msg = client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system or "Eres un asistente experto de HITL Lab.",
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text

    # ── IBM WatsonX ───────────────────────────────────────
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def _call_watsonx(self, prompt: str, system: str) -> str:
        from ibm_watsonx_ai.foundation_models import ModelInference
        model = ModelInference(
            model_id=self.model,
            api_client=None,  # usa WATSONX_API_KEY del env
            project_id=os.getenv("WATSONX_PROJECT_ID"),
            params={"max_new_tokens": 1024}
        )
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        return model.generate_text(full_prompt)

    # ── AWS Bedrock ───────────────────────────────────────
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def _call_bedrock(self, prompt: str, system: str) -> str:
        import boto3, json
        client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1")
            # credentials desde AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
        )
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "system": system,
            "messages": [{"role": "user", "content": prompt}]
        })
        response = client.invoke_model(modelId=self.model, body=body)
        return json.loads(response["body"].read())["content"][0]["text"]

    # ── Google Gemini ─────────────────────────────────────
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def _call_gemini(self, prompt: str, system: str) -> str:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel(self.model)
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        return model.generate_content(full_prompt).text

    # ── OpenAI ────────────────────────────────────────────
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def _call_openai(self, prompt: str, system: str) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    # ── ISO 22301: Fallback ───────────────────────────────
    def _fallback(self) -> str:
        return FALLBACK_RESPONSE

    # ── ISO 42001: Audit log ──────────────────────────────
    def _audit_log(self, prompt: str, response: str, latency: float):
        """
        Registra cada llamada al modelo.
        Requerido por ISO 42001 — trazabilidad de sistemas AI.
        """
        if not self.audit_enabled:
            return

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "provider": self.provider,
            "model": self.model,
            "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
            "prompt_chars": len(prompt),
            "response_chars": len(response),
            "latency_seconds": latency,
            "is_fallback": response == FALLBACK_RESPONSE,
        }

        try:
            os.makedirs(os.path.dirname(self.audit_path), exist_ok=True)
            with open(self.audit_path, "a") as f:
                f.write(json.dumps(record) + "\n")
        except Exception as e:
            log.error("audit_log_failed", error=str(e))

        log.info("ai_call", **record)
