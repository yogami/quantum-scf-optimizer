const fs = require('fs');
const path = require('path');
const https = require('https');

/**
 * OPENAI PROFESSIONAL TTS GENERATOR
 */

// 1. Manually parse .env to avoid dependencies
const envContent = fs.readFileSync('/Users/user1000/gitprojects/InstagramReelPoster/.env', 'utf8');
const env = {};
envContent.split('\n').forEach(line => {
    const [key, ...valueParts] = line.split('=');
    if (key && valueParts.length > 0) {
        let value = valueParts.join('=').trim();
        if (value.startsWith('"') && value.endsWith('"')) value = value.slice(1, -1);
        if (value.startsWith("'") && value.endsWith("'")) value = value.slice(1, -1);
        env[key.trim()] = value;
    }
});

const API_KEY = env.OPENAI_API_KEY;
const VOICE = "alloy"; // Professional neutral voice
const MODEL = "tts-1";

if (!API_KEY) {
    console.error('❌ Missing OPENAI_API_KEY in InstagramReelPoster .env');
    process.exit(1);
}

const scriptPath = path.join(__dirname, '../scripts/demo_v1_en.json');
const outputDir = path.join(__dirname, '../voiceovers_en_pro');

if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

async function synthesize() {
    console.log(`🎙️ Starting OpenAI Synthesis (${VOICE}) for CascadeGuard Demo...`);
    const script = JSON.parse(fs.readFileSync(scriptPath, 'utf8'));

    for (const segment of script) {
        const filePath = path.join(outputDir, `segment_${segment.id}.mp3`);
        console.log(`[Seg ${segment.id}] Synthesizing text: "${segment.text.substring(0, 30)}..."`);

        try {
            await new Promise((resolve, reject) => {
                const postData = JSON.stringify({
                    model: MODEL,
                    input: segment.text,
                    voice: VOICE,
                    response_format: 'mp3',
                    speed: 1.0
                });

                const options = {
                    hostname: 'api.openai.com',
                    port: 443,
                    path: '/v1/audio/speech',
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${API_KEY}`,
                        'Content-Type': 'application/json',
                        'Content-Length': Buffer.byteLength(postData)
                    }
                };

                const req = https.request(options, (res) => {
                    const chunks = [];
                    res.on('data', (d) => chunks.push(d));
                    res.on('end', () => {
                        if (res.statusCode !== 200) {
                            reject(new Error(`Status: ${res.statusCode} - ${Buffer.concat(chunks).toString()}`));
                            return;
                        }
                        fs.writeFileSync(filePath, Buffer.concat(chunks));
                        resolve(true);
                    });
                });

                req.on('error', (e) => reject(e));
                req.write(postData);
                req.end();
            });

            console.log(`✅ Saved: ${filePath}`);
        } catch (error) {
            console.error(`❌ Failed segment ${segment.id}:`, error.message);
        }
    }
    console.log('✨ All segments synthesized with professional voice.');
}

synthesize();
