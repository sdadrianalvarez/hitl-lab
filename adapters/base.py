import os, json, time, hashlib
from datetime import datetime, timezone
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential

MODEL_REGISTRY = {
    'claude':  'claude-sonnet-4-6',
    'watsonx': 'ibm/granite-13b-chat-v2',
    'bedrock': 'anthropic.claude-3-sonnet-20240229-v1:0',
    'gemini':  'gemini-1.5-pro',
    'openai':  'gpt-4o',
}
FALLBACK_RESPONSE = '[HITL-DRP] Servicio AI no disponible. RTO: 4 horas. soporte@hitl.mx'

class AIAdapter:
    def __init__(self, provider=None):
        self.provider = provider or os.getenv('PROVIDER', 'claude')
        self.model = MODEL_REGISTRY.get(self.provider, 'unknown')
        self.audit_path = os.getenv('AUDIT_LOG_PATH', '/home/jovyan/data/audit.jsonl')

    def complete(self, prompt, system=''):
        start = time.time()
        response = FALLBACK_RESPONSE
        try:
            if self.provider == 'claude':
                response = self._call_claude(prompt, system)
            elif self.provider == 'watsonx':
                response = self._call_watsonx(prompt, system)
            elif self.provider == 'bedrock':
                response = self._call_bedrock(prompt, system)
            elif self.provider == 'gemini':
                response = self._call_gemini(prompt, system)
            elif self.provider == 'openai':
                response = self._call_openai(prompt, system)
        except Exception as e:
            print(f'[ERROR] {self.provider}: {e}')
            response = FALLBACK_RESPONSE
        finally:
            self._audit_log(prompt, response, round(time.time()-start, 3))
        return response

    def _call_claude(self, prompt, system):
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        msg = client.messages.create(
            model=self.model, max_tokens=1024,
            system=system or 'Eres un asistente experto de HITL Lab.',
            messages=[{'role': 'user', 'content': prompt}])
        return msg.content[0].text

    def _call_watsonx(self, prompt, system):
        from ibm_watsonx_ai.foundation_models import ModelInference
        model = ModelInference(model_id=self.model,
            project_id=os.getenv('WATSONX_PROJECT_ID'),
            params={'max_new_tokens': 1024})
        return model.generate_text(f'{system}\n\n{prompt}' if system else prompt)

    def _call_bedrock(self, prompt, system):
        import boto3
        client = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION','us-east-1'))
        body = json.dumps({'anthropic_version':'bedrock-2023-05-31',
            'max_tokens':1024,'system':system,
            'messages':[{'role':'user','content':prompt}]})
        r = client.invoke_model(modelId=self.model, body=body)
        return json.loads(r['body'].read())['content'][0]['text']

    def _call_gemini(self, prompt, system):
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        m = genai.GenerativeModel(self.model)
        return m.generate_content(f'{system}\n\n{prompt}' if system else prompt).text

    def _call_openai(self, prompt, system):
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        r = client.chat.completions.create(model=self.model,
            messages=[{'role':'system','content':system},{'role':'user','content':prompt}])
        return r.choices[0].message.content

    def _audit_log(self, prompt, response, latency):
        record = {'timestamp': datetime.now(timezone.utc).isoformat(),
            'provider': self.provider, 'model': self.model,
            'prompt_hash': hashlib.sha256(prompt.encode()).hexdigest()[:16],
            'latency_seconds': latency,
            'is_fallback': response == FALLBACK_RESPONSE}
        try:
            os.makedirs(os.path.dirname(self.audit_path), exist_ok=True)
            with open(self.audit_path, 'a') as f:
                f.write(json.dumps(record) + '\n')
        except Exception:
            pass
