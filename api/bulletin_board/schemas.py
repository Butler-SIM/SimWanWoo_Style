from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)

from api.bulletin_board.serializers.bulletin_board import BulletinBoardListSerializer, BulletinBoardDetailSerializer, \
    BulletinBoardCreateSerializer


BULLETIN_BOARD_TAG = "bulletin_board"


class BulletinBoardSchema:
    bulletin_board_list_schema = extend_schema(
        tags=[BULLETIN_BOARD_TAG],
        summary=f" - 게시판 목록 조회 API_UPDATE : 2023-02-27",
        parameters=[
            OpenApiParameter(
                name="page_size",
                description=f"page_size 기본값 10.",
                required=False,
                type=int,
            ),
        ],
        responses=BulletinBoardListSerializer,
    )

    bulletin_board_detail_schema = extend_schema(
        tags=[BULLETIN_BOARD_TAG],
        summary=f" - 게시판 상세 조회 API_UPDATE : 2023-02-27",
        request=BulletinBoardDetailSerializer,
        responses=BulletinBoardDetailSerializer,
    )

    bulletin_board_create_schema = extend_schema(
        tags=[BULLETIN_BOARD_TAG],
        summary=f" - 게시글 생성 API_UPDATE : 2023-02-27",
        request=BulletinBoardCreateSerializer,
        responses=BulletinBoardCreateSerializer,
    )

    bulletin_board_update_schema = extend_schema(
        tags=[BULLETIN_BOARD_TAG],
        summary=f" - 게시글 수정 API_UPDATE : 2023-02-27",
        request=BulletinBoardDetailSerializer,
    )

    bulletin_board_delete_schema = extend_schema(
        tags=[BULLETIN_BOARD_TAG],
        summary=f" - 게시글 삭제 API_UPDATE : 2023-02-27",
        description="관리자 매거진 삭제",
    )

    article_schema_view = extend_schema_view(
        list=bulletin_board_list_schema,
        retrieve=bulletin_board_detail_schema,
        create=bulletin_board_create_schema,
        partial_update=bulletin_board_update_schema,
        destroy=bulletin_board_delete_schema,
    )


