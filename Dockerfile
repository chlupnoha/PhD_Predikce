FROM public.ecr.aws/lambda/python:3.8

# Install the function's dependencies using file requirements.txt
# from your project folder.

RUN pip install --no-cache-dir pandas catboost --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY trained_model_metrics.pickle ${LAMBDA_TASK_ROOT}
COPY data_transformation.py lambda_function.py ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]
