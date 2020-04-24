resource "aws_iam_role" "role" {
  name = "${var.function_name}-role"
  tags = merge(
    var.tags,
    {
      "Name" = "${var.function_name}-role"
    },
  )
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "policy" {
  name        = "${var.function_name}-policy"
  description = "${var.function_name} policy"
  policy      = var.policy_json
}

resource "aws_iam_role_policy_attachment" "policy_attachment_1" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.policy.arn
}

resource "aws_iam_role_policy_attachment" "policy_attachment_2" {
  role       = aws_iam_role.role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

