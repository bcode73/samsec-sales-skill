<!-- Source: https://docs.generateblocks.com/article/dynamic-data-options-overview/ , https://snippetclub.com/how-to-create-custom-dynamic-tags-in-generateblocks-2-0-a-complete-guide/ , https://learn.generatepress.com/developer-doc/generateblocks_dynamic_tag_output/ , https://docs.generateblocks.com/ -->

# GenerateBlocks Developer Reference — Dynamic Data, Dynamic Tags & Hooks

GenerateBlocks is a WordPress plugin. It has **no hosted REST API** and **no native outbound webhook**. Its programmatic surface is:

1. **WordPress core** — the WP REST API (`/wp-json/wp/v2/...`), application-password auth, and WP-CLI. GenerateBlocks block content lives in the `post_content` field as `generateblocks/`-namespaced block markup.
2. **GenerateBlocks' own public actions & filters** (PHP `add_action` / `add_filter`) and the **Dynamic Tag registration API** (`GenerateBlocks_Register_Dynamic_Tag`, 2.0+).

> Names and signatures below are reproduced from GenerateBlocks' public documentation and developer tutorials. GenerateBlocks 2.0 was a rewrite; confirm exact array keys, hook names, and callback signatures against your installed GenerateBlocks/GenerateBlocks Pro version before relying on them.

## Authentication quick-start (WordPress core, not GenerateBlocks-specific)

```bash
# Read a page's GenerateBlocks block markup with an application password
curl -s https://example.com/wp-json/wp/v2/pages/123 \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" | jq '.content.rendered'
```

Generate an application password under **Users → Profile → Application Passwords**. The token inherits that user's capabilities. To write block markup, `POST`/`PUT` to `/wp-json/wp/v2/pages/{id}` with a `content` field containing `generateblocks/`-namespaced block comments.

## Dynamic Data — options overview

*From the official Dynamic Data Options Overview docs.* Dynamic Data dynamically pulls the data associated with your posts, pages, users, and custom post types. It is available on the **Headline, Button, Image, and Container** blocks (Dynamic Data is a **Pro** feature).

### Data Source

Select **Current post** or a specific post type (posts, pages, products, custom types). You can designate a particular post, or leave it blank inside a Query Loop so each item resolves to its own post.

### Content Sources (Headline & Button)

- **Title** — outputs the post title
- **Excerpt** — configurable word length and optional "Read more" link
- **Post date** — published or updated date
- **Post Meta** — custom field values (incl. ACF; deeply-nested meta arrays are addressable by specifying the keys)
- **Comments number** — customizable text for zero / one / multiple comments
- **List of terms** — taxonomy-based, with separator options
- **Author meta** — user profile information
- **Email, Name, Nickname, First name, Last name** — user account data

### Image Sources (Image block)

- Featured image
- Post-meta image value
- Author avatar

### Background Images (Container block)

Container blocks can use featured images, post-meta images, and author avatars as backgrounds.

### Link Sources (Headline, Button, Image)

Single post, comments area, post-meta link, author archive, author-meta link, author email (with `mailto:` or `tel:` prefix options), and the image file.

## Dynamic Tags — custom registration (GenerateBlocks 2.0+)

*From the "Create Custom Dynamic Tags in GenerateBlocks 2.0" developer guide.* Dynamic tags are registered with the `GenerateBlocks_Register_Dynamic_Tag` class. Register on the `init` action.

### Core registration pattern

```php
function tct_register_dynamic_tags() {
    if ( ! class_exists( 'GenerateBlocks_Register_Dynamic_Tag' ) ) {
        return;
    }

    new GenerateBlocks_Register_Dynamic_Tag(
        [
            'title'    => __( 'Tag Name', 'textdomain' ),
            'tag'      => 'unique_tag_identifier',
            'type'     => 'post',
            'supports' => [ 'source' ],
            'return'   => 'callback_function_name',
        ]
    );
}
add_action( 'init', 'tct_register_dynamic_tags' );
```

### Tag definition array

| Key | Purpose |
|---|---|
| `title` | Display name shown in the block editor |
| `tag` | Unique identifier for the tag |
| `type` | Category grouping — e.g. `'post'`, `'author'`, `'elements'` |
| `supports` | Features the tag supports — e.g. `'source'`, `'image-size'` |
| `options` | Configuration fields rendered in the editor (select, text, number inputs) |
| `return` | Callback function reference that produces the output |

### Callback signature

```php
function callback_name( $options, $block, $instance ) {
    // ...build $content...
    return GenerateBlocks_Dynamic_Tag_Callbacks::output(
        $content,
        $options,
        $instance
    );
}
```

The `GenerateBlocks_Dynamic_Tag_Callbacks::output()` helper automatically handles truncation, string replacement, trimming, case modification, paragraph formatting, and link wrapping — so custom tags behave like built-in ones.

## Public filters

| Filter | Version | Purpose | Signature (best-effort) |
|---|---|---|---|
| `generateblocks_dynamic_tag_output` | 2.0+ | Modify the output of a dynamic tag | `( $output, $options )` |
| `generateblocks_dynamic_content_output` | 1.x (legacy) | Filter dynamic data output | `( $output )` |
| `generateblocks_image_url` | — | Filter the resolved image URL for dynamic images | `( $url )` |
| `generateblocks_dynamic_image_fallback` | — | Provide/modify the fallback when a dynamic image is missing | `( $fallback )` |
| `generateblocks_do_content` | — | Add content sources for dynamic CSS generation (so block CSS is generated for content rendered outside the main loop, e.g. shortcodes/templates) | `( $content )` |

```php
// Example: post-process dynamic tag output (2.0+)
add_filter( 'generateblocks_dynamic_tag_output', function ( $output, $options ) {
    return $output;
}, 10, 2 );

// Example: ensure GenerateBlocks generates CSS for content rendered via a custom source
add_filter( 'generateblocks_do_content', function ( $content ) {
    // append additional content whose blocks need CSS generated
    return $content;
} );
```

> `generateblocks_dynamic_tag_output` is documented on Learn GeneratePress (learn.generatepress.com/developer-doc/generateblocks_dynamic_tag_output) but that page is bot-protected (403 to automated fetch) — confirm the exact parameter list in your installed version or via the in-app developer docs.

## Block markup namespace

GenerateBlocks blocks are stored in `post_content` under the `generateblocks/` namespace. In the 2.0 rewrite the core blocks were unified (element/container, grid, text/headline, button, image, query, looper). Block names and attribute keys changed between 1.x and 2.x — **copy a real block from the editor as the source of truth** rather than hand-authoring from memory.

```html
<!-- wp:generateblocks/element {"uniqueId":"abcd1234","tagName":"div"} -->
<div class="gb-element-abcd1234"> ... </div>
<!-- /wp:generateblocks/element -->
```

## Gaps / not documented

- **No public hosted REST API** for GenerateBlocks objects — use the WordPress core REST API against posts/pages, whose `content` holds the `generateblocks/` block markup.
- **No native outbound webhook and no form block** — lead delivery rides on a paired form plugin, not GenerateBlocks.
- **No first-party Zapier/Make app** for GenerateBlocks itself.
- **No public GitHub repository** for the plugin — it's developed on the WordPress.org SVN/Trac; the maintainer's other Block Editor projects are on GitHub.
- Exact dynamic-tag `options`/`supports` keys, the full filter list, and 2.x block attribute schemas evolve per release. Confirm against `docs.generateblocks.com` and the installed version. Source pages: `dynamic-data-options-overview`, the SnippetClub 2.0 custom-tags guide, and `generateblocks_dynamic_tag_output` on Learn GeneratePress.
