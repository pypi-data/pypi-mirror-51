Wagtail UI Plus
============================
This Wagtail app provides several ui improvements to the Wagtail editor interface.

- Improved UI for StreamFields
- Improved UI for StreamBlocks nested inside StreamFields

Preview
-------

![Screenshot](https://raw.githubusercontent.com/davidcondenl/wagtailuiplus/master/screenshot.png)

Install
-------

- `pip install wagtailuiplus`
- Add `wagtailuiplus` to your installed apps

Example
-------
The following code was used in a `models.py` file to generate the above screenshot.
```
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.blocks import (
  CharBlock,
  StreamBlock,
  StructBlock,
  RichTextBlock,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class MyCharBlock(CharBlock):
    class Meta:
        icon = 'pilcrow'
        label = 'My char block'


class MyRichTextBlock(RichTextBlock):
    class Meta:
        icon = 'openquote'
        label = 'My rich text block'


class MyStreamBlock(StreamBlock):
    title = MyCharBlock()
    text = MyRichTextBlock()

    class Meta:
        label = 'My stream block'


class MyStructBlock(StructBlock):
    items = MyStreamBlock(required=False)

    class Meta:
        icon = 'list-ul'
        label = 'My struct block'


class HomePage(Page):
    my_stream_field = StreamField([
            ('my_title_block', MyCharBlock()),
            ('my_text_block', MyRichTextBlock()),
            ('my_struct_block', MyStructBlock()),
        ], blank=True, verbose_name='My stream field')

    content_panels = [
        StreamFieldPanel('my_stream_field'),
    ]

```
