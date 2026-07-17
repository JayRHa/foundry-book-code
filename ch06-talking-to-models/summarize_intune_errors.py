"""Chapter 06 — End to end: Foundry SDK plus structured output over real Intune error data.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

Setup:
    az login
    export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
"""

# summarize_intune_errors.py — end-to-end: Foundry SDK + structured output
import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

PROJECT_ENDPOINT = (
    "https://my-foundry-resource.services.ai.azure.com/api/projects/my-foundry-project"
)

device_errors = [
    "DEVICE-042: Win32 app 'SAP GUI' install failed, error 0x87D00668",
    "DEVICE-107: Compliance state noncompliant, BitLocker encryption not enabled",
    "DEVICE-113: Win32 app 'SAP GUI' install failed, error 0x87D00668",
    "DEVICE-201: Enrollment failed, user reached device limit",
    "DEVICE-233: Compliance state noncompliant, BitLocker encryption not enabled",
]

report_schema = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "top_causes": {"type": "array", "items": {"type": "string"}},
        "recommended_actions": {"type": "array", "items": {"type": "string"}},
        "affected_devices": {"type": "integer"},
    },
    "required": ["summary", "top_causes", "recommended_actions", "affected_devices"],
    "additionalProperties": False,
}

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential()
)
client = project.get_openai_client()

completion = client.chat.completions.create(
    model="gpt-5.1-mini",
    messages=[
        {
            "role": "system",
            "content": "You are an Intune support assistant. Summarize device errors "
                       "for an IT operations report. Be factual and concise.",
        },
        {"role": "user", "content": "Device errors:\n" + "\n".join(device_errors)},
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {"name": "intune_report", "strict": True, "schema": report_schema},
    },
)

report = json.loads(completion.choices[0].message.content)
print("Summary: ", report["summary"])
print("Devices affected:", report["affected_devices"])
print("Top causes:")
for cause in report["top_causes"]:
    print(" -", cause)
print("Recommended actions:")
for action in report["recommended_actions"]:
    print(" -", action)
