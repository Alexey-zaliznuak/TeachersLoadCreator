from functools import partial
from typing import Any, List, Optional, Union

from flet import Text as FletText
from flet import TextOverflow, TextThemeStyle, colors
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.text_span import TextSpan
from flet_core.types import (
    AnimationValue,
    FontWeight,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    TextAlign
)

from library.core.widgets.settings import PARAGRAPH_TEXT_SIZE, TITLE_TEXT_SIZE


__all__ = ['Text', 'TitleText']


class Text(FletText):
    def __init__(
        self,
        value: Optional[str] = None,
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # text-specific
        #
        spans: Optional[List[TextSpan]] = None,
        text_align: TextAlign = TextAlign.NONE,
        font_family: Optional[str] = None,
        size: OptionalNumber = PARAGRAPH_TEXT_SIZE,
        weight: Optional[FontWeight] = None,
        italic: Optional[bool] = None,
        style: Optional[TextThemeStyle] = None,
        max_lines: Optional[int] = None,
        overflow: TextOverflow = TextOverflow.NONE,
        selectable: Optional[bool] = True,
        no_wrap: Optional[bool] = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        semantics_label: Optional[str] = None,
    ):
        super().__init__(
            value=value,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            spans=spans,
            text_align=text_align,
            font_family=font_family,
            size=size,
            weight=weight,
            italic=italic,
            style=style,
            max_lines=max_lines,
            overflow=overflow,
            selectable=selectable,
            no_wrap=no_wrap,
            color=color,
            bgcolor=bgcolor,
            semantics_label=semantics_label,
        )


TitleText = partial(Text, size=TITLE_TEXT_SIZE)


class ErrorText(FletText):
    def __init__(self, text: str, *args, **kwargs):
        super().__init__(text, color=colors.RED_400)
