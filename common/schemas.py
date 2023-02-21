"""
api 문서 예시
"""

VERSION = {
    "V1": "V1",
    "V2": "V2",
    "V3": "V3",
    "V4": "V4",
}

# @extend_schema(
#         tags=['테스트'],
#         description='테스트를 위한 메소드입니다',
#         responses=GroupSerializer,
#         examples=[
#             OpenApiExample(
#                 response_only=True,
#                 summary="이거는 Response Body Example입니다.",
#                 name="success_example",
#                 value={
#                     "url": "https://dashboard.datamaker.io/",
#                     "name": "데이터메이커",
#                 },
#             ),
#         ],
#         parameters=[
#             OpenApiParameter(
#                 name="path_param",
#                 type=str,
#                 location=OpenApiParameter.PATH,
#                 description="아이디 입니다.",
#                 required=True,
#             ),
#             OpenApiParameter(
#                 name="text_param",
#                 type=str,
#                 description="text_param 입니다.",
#                 required=False,
#             ),
#             OpenApiParameter(
#                 name="select_param",
#                 type=str,
#                 description="first_param 입니다.",
# 								#enum : 받을 수 있는 값을 제한함
#                 enum=['선택1', '선택2', '선택3'],
#                 examples=[
#                     OpenApiExample(
#                         name="이것은 Select Parameter Example입니다.",
#                         summary="요약입니다",
#                         description="설명글은 길게 작성합니다",
#                         value="선택1",
#                     ),
#                     OpenApiExample(
#                         "이것은 Select Parameter Example2입니다.",
#                         summary="두번째 요약입니다",
#                         description="두번째 설명글은 더 길게 작성합니다",
#                         value="선택4",
#                     ),
#                 ],
#             ),
#             OpenApiParameter(
#                 name="date_param",
#                 type=OpenApiTypes.DATE,
#                 location=OpenApiParameter.QUERY,
#                 description="date filter",
#                 examples=[
#                     OpenApiExample(
#                         name="이것은 Query Parameter Example입니다.",
#                         summary="요약입니다",
#                         description="설명글은 길게 작성합니다",
#                         value="0000000",
#                     ),
#                     OpenApiExample(
#                         name="이것은 Query Parameter Example2입니다.",
#                         summary="두번째 요약입니다",
#                         description="두번째 설명글은 더 길게 작성합니다",
#                         value="00000001
#                         ",
#                     ),
#                 ],
#             ),
#         ],
#     )


# @extend_schema_view(
#     list=extend_schema(summary="이런식으로 class레벨 데코레이터로 문서 커스터마이징 가능하다.", tags=["사용자"]),
#     i_am_custom_api=extend_schema(
#         summary="@action API도 마찬가지로 class 데코레이터로 문서 커스터마이징 가능하다.",
#         tags=["사용자"],
#         request=CustomUserSerializer,
#         responses={status.HTTP_200_OK: CustomUserSerializer},
#     ),
# )
