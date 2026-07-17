"""Chapter 11 — Upload, start the job, poll it, deploy the result.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code
"""

# Upload training data and start an SFT fine-tuning job
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://<your-resource>.openai.azure.com/openai/v1/",
    api_key=os.environ["FOUNDRY_API_KEY"],  # or Entra ID auth as shown in Chapter 6
)

training = client.files.create(
    file=open("intune-errors-train.jsonl", "rb"),
    purpose="fine-tune",
)

job = client.fine_tuning.jobs.create(
    model="gpt-4.1-2025-04-14",
    training_file=training.id,
    suffix="intune-triage",
    seed=42,
)

job = client.fine_tuning.jobs.retrieve(job.id)
print(job.status)  # later: job.fine_tuned_model, e.g. gpt-4.1-2025-04-14.ft-<jobid>
