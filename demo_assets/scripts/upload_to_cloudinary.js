const fs = require('fs');
const path = require('path');
const https = require('https');
const crypto = require('crypto');

/**
 * CLOUDINARY UPLOADER (ZERO-DEPENDENCY)
 */

// 1. Setup
const CLOUD_NAME = "djol0rpn5";
const API_KEY = "888753318981763";
const API_SECRET = "HqTbA8IE_o6CHbenhKb_iiKXOwo";

const filePath = '/Users/user1000/gitprojects/cascade-guard-scf/demo_assets/output/CascadeGuard_Industrial_Demo_EN.mp4';
const timestamp = Math.floor(Date.now() / 1000);
const folder = "cascade-guard/demo";
const publicId = `industrial_demo_en_${timestamp}`;

// 2. Generate Signature
// Params to sign: folder, public_id, timestamp (alphabetical order)
const strToSign = `folder=${folder}&public_id=${publicId}&timestamp=${timestamp}${API_SECRET}`;
const signature = crypto.createHash('sha1').update(strToSign).digest('hex');

console.log(`🚀 Uploading to Cloudinary as ${publicId}...`);

async function upload() {
    const boundary = `----${crypto.randomBytes(16).toString('hex')}`;
    const url = `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/video/upload`;

    const fileBuffer = fs.readFileSync(filePath);

    const parts = [
        { name: 'api_key', value: API_KEY },
        { name: 'timestamp', value: timestamp },
        { name: 'folder', value: folder },
        { name: 'public_id', value: publicId },
        { name: 'signature', value: signature },
    ];

    let body = '';
    for (const part of parts) {
        body += `--${boundary}\r\n`;
        body += `Content-Disposition: form-data; name="${part.name}"\r\n\r\n`;
        body += `${part.value}\r\n`;
    }

    body += `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="file"; filename="demo.mp4"\r\n`;
    body += `Content-Type: video/mp4\r\n\r\n`;

    const footer = `\r\n--${boundary}--\r\n`;

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': `multipart/form-data; boundary=${boundary}`,
        }
    };

    const req = https.request(url, options, (res) => {
        let responseBody = '';
        res.on('data', chunk => responseBody += chunk);
        res.on('end', () => {
            const data = JSON.parse(responseBody);
            if (data.secure_url) {
                console.log('\n✨ UPLOAD SUCCESSFUL!');
                console.log('🔗 URL:', data.secure_url);
                fs.writeFileSync('/Users/user1000/gitprojects/cascade-guard-scf/demo_assets/output/cloudinary_url.txt', data.secure_url);
            } else {
                console.error('\n❌ UPLOAD FAILED:', data.error ? data.error.message : responseBody);
            }
        });
    });

    req.on('error', (e) => console.error('❌ Request Error:', e));

    req.write(Buffer.from(body));
    req.write(fileBuffer);
    req.write(Buffer.from(footer));
    req.end();
}

upload();
