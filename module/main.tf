terraform {
  backend "s3" {
  }
}

data "aws_caller_identity" "current" {
}

resource "aws_lambda_function" "disable-key" {
  filename         = disable-key.zip
  function_name    = var.function_name
  role             = aws_iam_role.role.arn
  handler          = "index.handler"
  source_code_hash = filebase64sha256(var.package_filename)
  runtime          = var.runtime
  timeout          = 10
  memory_size      = 512

  tags = merge(
    var.tags,
    {
      "Name" = var.function_name
    },
  )

  environment {
    variables = var.variables
  }
}

resource "aws_lambda_permission" "invoke" {
  function_name = aws_lambda_function.lambda.function_name

  action         = "lambda:InvokeFunction"
  principal      = ".${var.aws_region}.amazonaws.com"
  source_account = data.aws_caller_identity.current.account_id
}

