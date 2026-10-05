# Deploy Mimulus Explorer on the existing cPanel host

This mirrors the deployment pattern already used for `cube.arctopia.no`.

Target subdomain:

`mimulus.arctopia.no`

Recommended document root:

`/public_html/Mimulus`

## Option A — GitHub Actions + FTPS

The workflow `.github/workflows/deploy-mimulus-cpanel.yml` builds a deploy package and uploads it over FTPS.

Required GitHub secrets:

- `ARCTOPIA_FTP_SERVER`
- `ARCTOPIA_FTP_USERNAME`
- `ARCTOPIA_FTP_PASSWORD`
- `MIMULUS_FTP_SERVER_DIR` — the FTP-visible path corresponding to the Mimulus document root; it must end in `/`
- `MIMULUS_OPENAI_API_KEY`

Optional secret:

- `MIMULUS_EXPLORER_TOKEN` — shared access token for the Explorer. Recommended if the endpoint is internet-accessible because API usage is billed to the key owner.

Optional repository variables:

- `MIMULUS_FAST_MODEL` — defaults to `gpt-6-luna`
- `MIMULUS_DEEP_MODEL` — defaults to `gpt-6.1-sol`

Run the workflow manually with `dry_run=true` first. Inspect the file plan. Then run again with `dry_run=false` to upload.

The workflow creates the following server layout:

```text
/public_html/Mimulus/
  index.html
  .htaccess
  DEPLOYMENT.txt
  api/
    explore.php
    config.php
```

`config.php` is generated during the workflow from GitHub Secrets and is denied from direct web access by `.htaccess`. No API key is committed to Git.

## Option B — manual upload, like Cube

Create the subdomain in cPanel and point it at `/public_html/Mimulus`.

Build the folder with:

- `explorer/index.html` copied to `/public_html/Mimulus/index.html`
- `hosting/cpanel/.htaccess` copied to `/public_html/Mimulus/.htaccess`
- `hosting/cpanel/api/explore.php` copied to `/public_html/Mimulus/api/explore.php`
- `hosting/cpanel/api/config.example.php` copied to `/public_html/Mimulus/api/config.php`, then edit only the server copy and insert the API key there

Do **not** commit the filled `config.php` back to GitHub.

## Runtime path

The browser posts to:

`/api/explore`

Apache rewrites that internally to:

`/api/explore.php`

The PHP endpoint then calls OpenAI's Responses API server-side. The browser never receives the OpenAI key.

## PHP requirements

The endpoint intentionally uses PHP syntax compatible with older PHP 7.x hosts. It requires:

- PHP cURL extension
- HTTPS outbound requests
- `mod_rewrite` for the clean `/api/explore` route

If `mod_rewrite` is unavailable, the frontend can be changed to call `/api/explore.php` directly.

## Evidence boundary

This is the naturalistic **Mimulus Explorer**, not the blind f113v run.

Every output remains classified as `EXPLORATORY_DECODER_OUTPUT`. A later translation or paraphrase of an Explorer output is lineage-dependent and cannot count as independent decoder agreement.
