# Component templates

Copy-paste starting points for a new snippet, block, or section, matching the
conventions in AGENTS.md (LiquidDoc header, {% stylesheet %}/{% javascript %} tags,
{% schema %} shape). Start from the closest template below rather than from scratch.

## Examples per kind of asset

### `snippet`

```liquid
{% doc %}
  Renders a responsive image that might be wrapped in a link.

  When `width`, `height` and `crop` are provided, the image will be rendered
  with a fixed aspect ratio.

  Serves as an example of how to use the `image_url` filter and `image_tag` filter
  as well as how you can use LiquidDoc to document your code.

  @param {image} image - The image to be rendered
  @param {string} [url] - An optional destination URL for the image
  @param {string} [css_class] - Optional class to be added to the image wrapper
  @param {number} [width] - The highest resolution width of the image to be rendered
  @param {number} [height] - The highest resolution height of the image to be rendered
  @param {string} [crop] - The crop position of the image

  @example
  {% render 'image', image: product.featured_image %}
  {% render 'image', image: product.featured_image, url: product.url %}
  {% render 'image',
    css_class: 'product__image',
    image: product.featured_image,
    url: product.url,
    width: 1200,
    height: 800,
    crop: 'center',
  %}
{% enddoc %}

{% liquid
  unless height
    assign width = width | default: image.width
  endunless

  if url
    assign wrapper = 'a'
  else
    assign wrapper = 'div'
  endif
%}

<{{ wrapper }}
  class="image {{ css_class }}"
  {% if url %}
    href="{{ url }}"
  {% endif %}
>
  {{ image | image_url: width: width, height: height, crop: crop | image_tag }}
</{{ wrapper }}>

{% stylesheet %}
  .image {
    display: block;
    position: relative;
    overflow: hidden;
    width: 100%;
    height: auto;
  }

  .image > img {
    width: 100%;
    height: auto;
  }
{% endstylesheet %}

{% javascript %}
  function doSomething() {
    // example
  }
  doSomething()
{% endjavascript %}

```

### `block`

#### Text

```liquid
{% doc %}
  Renders a text block.

  @example
  {% content_for 'block', type: 'text', id: 'text' %}
{% enddoc %}

<div
  class="text {{ block.settings.text_style }}"
  style="--text-align: {{ block.settings.alignment }}"
  {{ block.shopify_attributes }}
>
  {{ block.settings.text }}
</div>

{% stylesheet %}
  .text {
    text-align: var(--text-align);
  }
  .text--title {
    font-size: 2rem;
    font-weight: 700;
  }
  .text--subtitle {
    font-size: 1.5rem;
  }
{% endstylesheet %}

{% schema %}
{
  "name": "t:general.text",
  "settings": [
    {
      "type": "text",
      "id": "text",
      "label": "t:labels.text",
      "default": "Text"
    },
    {
      "type": "select",
      "id": "text_style",
      "label": "t:labels.text_style",
      "options": [
        { "value": "text--title", "label": "t:options.text_style.title" },
        { "value": "text--subtitle", "label": "t:options.text_style.subtitle" },
        { "value": "text--normal", "label": "t:options.text_style.normal" }
      ],
      "default": "text--title"
    },
    {
      "type": "text_alignment",
      "id": "alignment",
      "label": "t:labels.alignment",
      "default": "left"
    }
  ],
  "presets": [{ "name": "t:general.text" }]
}
{% endschema %}
```

#### Group

```liquid
{% doc %}
  Renders a group of blocks with configurable layout direction, gap and
  alignment.

  All settings apply to only one dimension to reduce configuration complexity.

  This component is a wrapper concerned only with rendering its children in
  the specified layout direction with appropriate padding and alignment.

  @example
  {% content_for 'block', type: 'group', id: 'group' %}
{% enddoc %}

<div
  class="group {{ block.settings.layout_direction }}"
  style="
    --padding: {{ block.settings.padding }}px;
    --alignment: {{ block.settings.alignment }};
  "
  {{ block.shopify_attributes }}
>
  {% content_for 'blocks' %}
</div>

{% stylesheet %}
  .group {
    display: flex;
    flex-wrap: nowrap;
    overflow: hidden;
    width: 100%;
  }
  .group--horizontal {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 0 var(--padding);
  }
  .group--vertical {
    flex-direction: column;
    align-items: var(--alignment);
    padding: var(--padding) 0;
  }
{% endstylesheet %}

{% schema %}
{
  "name": "t:general.group",
  "blocks": [{ "type": "@theme" }],
  "settings": [
    {
      "type": "select",
      "id": "layout_direction",
      "label": "t:labels.layout_direction",
      "default": "group--vertical",
      "options": [
        { "value": "group--horizontal", "label": "t:options.direction.horizontal" },
        { "value": "group--vertical", "label": "t:options.direction.vertical" }
      ]
    },
    {
      "visible_if": "{{ block.settings.layout_direction == 'group--vertical' }}",
      "type": "select",
      "id": "alignment",
      "label": "t:labels.alignment",
      "default": "flex-start",
      "options": [
        { "value": "flex-start", "label": "t:options.alignment.left" },
        { "value": "center", "label": "t:options.alignment.center" },
        { "value": "flex-end", "label": "t:options.alignment.right" }
      ]
    },
    {
      "type": "range",
      "id": "padding",
      "label": "t:labels.padding",
      "default": 0,
      "min": 0,
      "max": 200,
      "step": 2,
      "unit": "px"
    }
  ],
  "presets": [
    {
      "name": "t:general.column",
      "category": "t:general.layout",
      "settings": {
        "layout_direction": "group--vertical",
        "alignment": "flex-start",
        "padding": 0
      }
    },
    {
      "name": "t:general.row",
      "category": "t:general.layout",
      "settings": {
        "layout_direction": "group--horizontal",
        "padding": 0
      }
    }
  ]
}
{% endschema %}
```

### `section`

```liquid
<div class="example-section full-width">
  {% if section.settings.background_image %}
    <div class="example-section__background">
      {{ section.settings.background_image | image_url: width: 2000 | image_tag }}
    </div>
  {% endif %}

  <div class="custom-section__content">
    {% content_for 'blocks' %}
  </div>
</div>

{% stylesheet %}
  .example-section {
    position: relative;
    overflow: hidden;
    width: 100%;
  }
  .example-section__background {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: -1;
    overflow: hidden;
  }
  .example-section__background img {
    position: absolute;
    width: 100%;
    height: auto;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  .example-section__content {
    display: grid;
    grid-template-columns: var(--content-grid);
  }

  .example-section__content > * {
    grid-column: 2;
  }
{% endstylesheet %}

{% schema %}
{
  "name": "t:general.custom_section",
  "blocks": [{ "type": "@theme" }],
  "settings": [
    {
      "type": "image_picker",
      "id": "background_image",
      "label": "t:labels.background"
    }
  ],
  "presets": [
    {
      "name": "t:general.custom_section"
    }
  ]
}
{% endschema %}
```

