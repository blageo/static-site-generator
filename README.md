# static-site-generator

A Python static site generator that converts Markdown content into a deployable HTML site. Built from scratch as part of the [Boot.dev](https://boot.dev) backend development curriculum — and currently deployed in production to serve internal IT documentation at a client site.

No dependencies. Just Python and a shell.

## How it works

Point it at a directory of Markdown files and a single HTML template, and it walks the content tree, parses each file into an HTML node tree, and writes out a mirrored directory of `.html` files into `docs/`.

The Markdown parser is built by hand — no libraries. It handles headings, paragraphs, code blocks, blockquotes, ordered and unordered lists, and inline formatting (bold, italic, links, images, code).

```
content/         <- your Markdown files go here
static/          <- CSS, images, anything static
template.html    <- single template with {{ Title }} and {{ Content }} placeholders
docs/            <- generated output (what you serve/deploy)
```

## Usage

To build the site:

```bash
./build.sh
```

To build and serve locally:

```bash
./main.sh
# then open http://localhost:8888
```

The build script passes a basepath argument for deployments where the site lives at a subdirectory rather than the root (e.g. GitHub Pages project sites).

## Running tests

```bash
./test.sh
```

## Deploying

The output lands in `docs/`, which is what GitHub Pages expects if you configure it to serve from that folder. A `.nojekyll` file is automatically created on each build so GitHub Pages doesn't strip files with underscores in the name.

For other hosts, just serve the `docs/` directory as a static site.
