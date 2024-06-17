const express = require('express');
const path = require('path');
const fs = require('fs');
const marked = require('marked');

const app = express();
const port = 3000;

// Middleware to serve static files
app.use('/images', express.static(path.join(__dirname, 'images')));

// Route to serve the html file
app.get('/', async (req, res) => {
    try {
        // read styles.css file
        const styles = path.join(__dirname, 'styles.css');
        const stylesContent = await fs.promises.readFile(styles, 'utf8');

        // code to read and process the html file
        const data = path.join(__dirname, 'data.html');
        const dataContent = await fs.promises.readFile(data, 'utf8');
        // const htmlContent = marked.parse(dataContent);

        res.send(`
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    ${stylesContent}
                </style>
                <title>Markdown Preview</title>
            </head>
            <body>
                ${dataContent}
            </body>
            </html>
        `);
    } catch (err) {
        res.status(500).send('Error reading markdown file');
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
