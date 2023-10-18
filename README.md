steps:
- name: 'gcr.io/cloud-builders/gcloud'
    args:
    - 'run'
    - 'deploy'
    - 'cloudrunservice'
    - '--image'
    - 'gcr.io/PROJECT_ID/IMAGE'
    - '--region'
    - 'REGION_TO_DEPLOY'
    - '--platform'
    - 'managed'
    - '--allow-unauthenticated'
artifacts:
    objects:
    location: 'gs://example-bucket'
    paths: ['*']

gcloud builds submit --gcs-source-staging-dir="gs://example-bucket/cloudbuild-custom" --config cloudbuild.yaml