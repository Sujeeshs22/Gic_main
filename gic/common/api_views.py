from rest_framework import viewsets, status
from rest_framework.response import Response
from common_config_app.views import generate_response
from .api_serializers import FileUploadSerializer, UserSerializer
import pandas as pd
from .models import *


class FileUploadViewset(viewsets.ViewSet):
    serializer_class = FileUploadSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            file = serializer.validated_data["file"]

            if not file.name.endswith(".csv"):
                return Response(
                    generate_response(False, "File should be in CSV format", []),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                df = pd.read_csv(file)
            except Exception as e:
                return Response(
                    generate_response(False, f"Failed to read CSV: {str(e)}", []),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            success_count = 0
            errors = []

            for index, row in df.iterrows():
                row_data = {
                    "name": row.get("name", "").strip(),
                    "email": row.get("email", "").strip(),
                    "age": row.get("age", ""),
                }

                serializer = UserSerializer(data=row_data)
                if serializer.is_valid():
                    if not User.objects.filter(email=row_data["email"]).exists():
                        User.objects.create(
                            name=row_data["name"],
                            email=row_data["email"],
                            age=row_data["age"],
                        )
                        success_count += 1
                    else:
                        errors.append(
                            {
                                "row": index + 1,
                                "errors": {"message": "duplicate email"},
                                "data": row_data,
                            }
                        )
                else:
                    errors.append(
                        {
                            "row": index + 1,
                            "errors": serializer.errors,
                            "data": row_data,
                        }
                    )

            return Response(
                generate_response(
                    True,
                    "File upload Successfull",
                    {
                        "saved_records": success_count,
                        "records_rejected": len(errors),
                        "errors": errors,
                    },
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            response_data = generate_response(False, [], f"An error occurred: {str(e)}")
            return Response(response_data, status=500)
