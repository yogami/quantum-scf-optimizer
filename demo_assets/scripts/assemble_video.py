import os
import subprocess

voiceovers_dir = "/Users/user1000/gitprojects/cascade-guard-scf/demo_assets/voiceovers_en_pro"
bg_music = "/Users/user1000/gitprojects/cascade-guard-scf/demo_assets/piano_bg.mp3"
webp_video = "/Users/user1000/.gemini/antigravity/brain/3546fa56-fd0a-4fcd-9a9a-c83dcb95b043/cascadeguard_demo_recording_1769584367656.webp"
output_audio = "/Users/user1000/gitprojects/cascade-guard-scf/demo_assets/output/final_audio.mp3"
output_video_tmp = "/Users/user1000/gitprojects/cascade-guard-scf/demo_assets/output/final_video_tmp.mp4"
output_video = "/Users/user1000/gitprojects/cascade-guard-scf/demo_assets/output/final_demo.mp4"

# Timings from script
timings = [0, 18, 36, 54, 72]
segments = [f"{voiceovers_dir}/segment_{i+1}.mp3" for i in range(5)]

# Build FFmpeg command for audio
filter_complex_audio = ""
for i in range(len(segments)):
    filter_complex_audio += f"[{i}]adelay={timings[i]*1000}|{timings[i]*1000}[a{i}];"

filter_complex_audio += "".join([f"[a{i}]" for i in range(len(segments))])
filter_complex_audio += f"amix=inputs={len(segments)}:dropout_transition=0:normalize=0[voice];"
filter_complex_audio += f"[5]volume=0.1[bg];" # Gentle piano
filter_complex_audio += f"[voice][bg]amix=inputs=2:dropout_transition=100[out]"

cmd_audio = [
    "ffmpeg", "-y",
    "-i", segments[0], "-i", segments[1], "-i", segments[2], "-i", segments[3], "-i", segments[4],
    "-i", bg_music,
    "-filter_complex", filter_complex_audio,
    "-map", "[out]",
    "-t", "87",
    output_audio
]

print("Merging audio...")
subprocess.run(cmd_audio)

# Convert webp to mp4 and scale to match audio duration
# First, let's get the webp duration if possible, or just force it to 87s
print("Assembling final video...")
cmd_final = [
    "ffmpeg", "-y",
    "-i", webp_video,
    "-i", output_audio,
    "-filter_complex", "[0:v]settb=1/AVTB,setpts=PTS*1.0[v]", # Adjust PTS if needed, but let's try 1.0 first
    "-map", "[v]",
    "-map", "1:a",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    output_video
]

subprocess.run(cmd_final)
print(f"Done! Final video at {output_video}")
