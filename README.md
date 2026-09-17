# Prof. Kern Tutoring

This is the GitHub Pages site for Prof. Kern Tutoring.

## Files
- `index.html` — home page with lesson format, policies, billing, and collaboration information
- `about.html` — about page
- `schedule.html` — schedule a session page
- `contact.html` — contact page
- `styles.css` — styling
- `script.js` — mobile navigation

## Important
The Contact page embeds a Google Form for sending messages.

The Schedule a Session page embeds:
`https://koalendar.com/e/tutoring-with-zoe`

## Local development

Python 3 is the only local dependency. Start the development server from this folder:

```powershell
python dev-server.py
```

Open `http://127.0.0.1:8000` in a browser. Changes to `index.html`, `styles.css`, or `script.js` are detected automatically and reload the page. Press `Ctrl+C` in the server terminal to stop it.

## GitHub Pages deployment

The `CNAME` file configures the site for `www.zoekay.com`. In the GitHub repository, open **Settings > Pages**, choose **Deploy from a branch**, select `main` and `/ (root)`, and save. Enter `www.zoekay.com` as the custom domain.

At the domain provider, create these DNS records:

- `www` CNAME pointing to `sunkiss115.github.io`
- `@` A pointing to `185.199.108.153`
- `@` A pointing to `185.199.109.153`
- `@` A pointing to `185.199.110.153`
- `@` A pointing to `185.199.111.153`

Remove conflicting A, AAAA, or URL-forwarding records for `@` and `www`. Enable **Enforce HTTPS** in GitHub Pages after DNS finishes propagating.
