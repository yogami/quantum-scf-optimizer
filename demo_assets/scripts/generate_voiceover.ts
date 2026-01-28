import fs from 'fs';
import path from 'path';
import https from 'https';
import dotenv from 'dotenv';

/**
 * PURE NODEJS GENERATOR (MINIMAL DEPENDENCIES)
 */

// 1. Setup - Point to the InstagramReelPoster .env for keys
dotenv.config({ path: '/Users/user1000/gitprojects/InstagramReelPoster/.env' });

const API_KEY = process.env.FISH_AUDIO_API_KEY;
const VOICE_ID = process.env.FISH_AUDIO_VOICE_ID;
const BASE_URL = 'api.fish.audio';

if (!API_KEY || !VOICE_ID) {
    console.error('❌ Missing FISH_AUDIO keys in InstagramReelPoster .env');
    process.exit(1);
}

const scriptPath = path.join(__dirname, '../scripts/demo_v1_en.json');
const outputDir = path.join(__dirname, '../voiceovers_en');

async function synthesize() {
    console.log('🎙️ Starting Synthesis for CascadeGuard Demo...');
    const script = JSON.parse(fs.readFileSync(scriptPath, 'utf8'));

    for (const segment of script) {
        const filePath = path.join(outputDir, `segment_${segment.id}.mp3`);
        console.log(`[Seg ${segment.id}] Synthesizing commentary...`);

        try {
            await new Promise((resolve, reject) => {
                const postData = JSON.stringify({
                    text: segment.text,
                    reference_id: VOICE_ID,
                    format: 'mp3',
                    speed: 1.0,
                    pitch: 1.0
                });

                const options = {
                    hostname: BASE_URL,
                    port: 443,
                    path: '/v1/tts',
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${API_KEY}`,
                        'Content-Type': 'application/json',
                        'Content-Length': postData.length
                    }
                };

                const req = https.request(options, (res) => {
                    const chunks: any[] = [];
                    res.on('data', (d) => chunks.push(d));
                    res.on('end', () => {
                        if (res.statusCode !== 200) {
                            reject(new Error(`Status: ${res.statusCode}`));
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
        } catch (error: any) {
            console.error(`❌ Failed segment ${segment.id}:`, error.message);
        }
    }
    console.log('✨ All segments synthesized.');
}

synthesize();
