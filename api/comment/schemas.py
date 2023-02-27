from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)

from api.comment.serializers.comment import CommentListSerializer, CommentCreateSerializer, CommentDetailSerializer, \
    CommentUpdateSerializer
from api.comment.serializers.reply import CommentReplyListSerializer, CommentReplyCreateSerializer, \
    CommentReplyDetailSerializer, CommentReplyUpdateSerializer

COMMENT_TAG = "board-comments"
COMMENT_REPLY_TAG = "board-comments-replies"


class CommentSchema:
    comment_list_schema = extend_schema(
        tags=[COMMENT_TAG],
        summary=f" -  댓글 목록 조회 API_UPDATE : 2023-02-27",
        parameters=[
            OpenApiParameter(
                name="bulletin_board_id",
                description="게시판 id값 필수 입력",
                required=True,
                type=int,
            ),
            OpenApiParameter(
                name="page_size",
                description=f"page_size 기본값 10.",
                required=False,
                type=int,
            ),
        ],
        responses=CommentListSerializer,
    )

    comment_create_schema = extend_schema(
        tags=[COMMENT_TAG],
        summary=f" -  댓글 생성 API_UPDATE : 2023-02-27",
        request=CommentCreateSerializer,
        responses=CommentDetailSerializer,
    )

    comment_detail_schema = extend_schema(
        tags=[COMMENT_TAG],
        summary=f" - s 댓글 상세 조회 API_UPDATE : 2023-02-27",
        responses=CommentDetailSerializer,
    )

    comment_detail_update_schema = extend_schema(
        tags=[COMMENT_TAG],
        summary=f" - 댓글 수정 API_UPDATE : 2023-02-27",
        description="댓글 수정\n\n작성자만 수정 가능합니다\n\n댓글 삭제 state : DELETE",
        request=CommentUpdateSerializer,
        responses=CommentDetailSerializer,
    )

    comment_schema_view = extend_schema_view(
        list=comment_list_schema,
        create=comment_create_schema,
        retrieve=comment_detail_schema,
        update=comment_detail_update_schema,
        partial_update=comment_detail_update_schema,
    )

    comment_detail_schema_view = extend_schema_view()


class CommentReplySchema:
    comment_reply_list_schema = extend_schema(
        tags=[COMMENT_REPLY_TAG],
        summary=f" -  대댓글 목록 조회 API_UPDATE : 2023-02-27",
        parameters=[
            OpenApiParameter(
                name="limit",
                description=f"기본값 10",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="offset",
                description=f"대댓글 기본값 1로 시작(빈값인 경우 1)\n\n"
                f"댓글 가장 처음 달린 대댓글은 댓글에서 조회되기때문에 offset이 0이 아닌 1부터 시작 \n\n"
                f"페이징시 limit가 기본값(10)이면 offset=1은 1페이지 offset=11은 2페이지",
                required=False,
                type=int,
            ),
        ],
        responses=CommentReplyListSerializer,
    )

    comment_reply_create_schema = extend_schema(
        tags=[COMMENT_REPLY_TAG],
        summary=f" -  대댓글 생성 API_UPDATE : 2023-02-27",
        request=CommentReplyCreateSerializer,
        responses=CommentReplyDetailSerializer,
    )

    comment_reply_detail_schema = extend_schema(
        tags=[COMMENT_REPLY_TAG],
        summary=f" -  대댓글 상세 조회 API_UPDATE : 2023-02-27",
        responses=CommentReplyDetailSerializer,
    )

    comment_reply_detail_update_schema = extend_schema(
        tags=[COMMENT_REPLY_TAG],
        summary=f" -  대댓글 수정 API_UPDATE : 2023-02-27",
        description=" 대댓글 수정\n\n작성자만 수정 가능합니다\n\n대댓글 삭제 state : DELETE",
        request=CommentReplyUpdateSerializer,
        responses=CommentReplyDetailSerializer,
    )

    comment_reply_schema_view = extend_schema_view(
        list=comment_reply_list_schema,
        create=comment_reply_create_schema,
        retrieve=comment_reply_detail_schema,
        update=comment_reply_detail_update_schema,
        partial_update=comment_reply_detail_update_schema,
    )


