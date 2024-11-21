import lzma
import googlemaps
import os
import json
from dotenv import load_dotenv
from chatlas import ChatOpenAI

import ffmpeg
from typing import TypedDict
import instaloader
import whisper

load_dotenv()

here = os.path.dirname(os.path.abspath(__file__))
insta_profiles = "insta_profiles"
os.makedirs(insta_profiles, exist_ok=True)
os.chdir(insta_profiles)

insta_profile_names = [
    "notboredindc",
    "thingstododc",
    "eventsdc",
    "washingtonbucketlist",
    "4dmvkids",
    "kidfriendlydc",
    "mommypoppinsdc",
]
insta_profile_names = [
    "4dmvkids",
]

prompt_file = os.path.join(here, "prompts", "01-system.txt")
prompt_file = os.path.join(here, "prompt.md")
with open(prompt_file, "r") as f:
    system_prompt = f.read().replace("\n", " ").strip()


if True:
    # Get instance
    L = instaloader.Instaloader()

    # Optionally, login or load session
    print("Log in...")
    L.login("bschloerke", os.getenv("INSTA_PASSWORD"))

    print("Making profile objects...")
    insta_profs = [
        instaloader.Profile.from_username(L.context, name)
        for name in insta_profile_names
    ]

    print("Downloading profiles...")
    L.download_profiles(
        insta_profs,
        fast_update=True,
        reels=True,
        posts=True,
        profile_pic=True,
        max_count=5,
    )
    # L.download_reels(prof, fast_update=True)
    # prof_reels = prof.get_reels()


def extract_audio_from_video(video_path, audio_path):
    # Use ffmpeg to extract audio
    (
        ffmpeg.input(video_path)
        .output(
            audio_path,
            vn=None,  # Exclude video stream
            loglevel="error",
            **{
                # Use 64k bitrate for smaller file
                "b:a": "64k",
                # Only output one channel, again for smaller file
                "ac": "1",
            },
        )
        .run(overwrite_output=True)
    )


# Example usage
# video_path = "downloaded_reel/2024-09-16_13-34-25_UTC.mp4"
# audio_path = "output_audio.aac"  # Choose .aac, .mp3, or another audio format

# import progressbar
# profile_bar = progressbar.ProgressBar(
#     maxval=len(insta_profile_names),
#     widgets=[
#         progressbar.Bar(),
#         " ",
#         progressbar.Counter(),
#         "/",
#         str(len(insta_profile_names)),
#         " ",
#         progressbar.AdaptiveETA(),
#     ],
# ).start()
# profile_bar.finish()

# Load the model
model: whisper.Whisper | None = None


def transcribe_audio(file: str):
    global model
    if model is None:
        print("Loading model...")
        model = whisper.load_model("tiny")
    return model.transcribe(file)


print("Processing audio...")
posts = []
for insta_profile_name in insta_profile_names:
    prof_dir = os.path.join(here, insta_profiles, insta_profile_name)
    profile_files = [os.path.join(prof_dir, file) for file in os.listdir(prof_dir)]

    # profile_bar.update(insta_profile_names.index(insta_profile_name) + 1)
    print(
        f"\n{insta_profile_name}... "
        f"{insta_profile_names.index(insta_profile_name) + 1}"
        "/"
        f"{len(insta_profile_names)}",
    )

    mp4_files = [file for file in profile_files if file.endswith(".mp4")]

    for mp4_file in mp4_files:
        # Quit if audio file already exists
        print(
            f"Processing video {os.path.basename(mp4_file)}... "
            f"{mp4_files.index(mp4_file) + 1}"
            "/"
            f"{len(mp4_files)}",
        )

        acc_file = mp4_file.replace(".mp4", ".aac")
        if not os.path.exists(acc_file):
            print("Extracting audio from video...")
            extract_audio_from_video(mp4_file, acc_file)

        audio_captions_file = mp4_file.replace(".mp4", "-audio.txt")
        if not os.path.exists(audio_captions_file):
            print("Transcribe audio...")
            result = transcribe_audio(acc_file)
            with open(audio_captions_file, "w") as f:
                f.write(result["text"])

        caption_file = mp4_file.replace(".mp4", ".txt")
        processed_file = mp4_file.replace(".mp4", "-processed.json")

        if not os.path.exists(processed_file):
            print("Extracting from video...")
            chat = ChatOpenAI(
                model="gpt-4o-mini",
                system_prompt=system_prompt,
            )

            # [
            #     {
            #         "place_id": 321070593,
            #         "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
            #         "osm_type": "way",
            #         "osm_id": 66418605,
            #         "lat": "38.88818305",
            #         "lon": "-77.01663726740057",
            #         "category": "tourism",
            #         "type": "museum",
            #         "place_rank": 30,
            #         "importance": 0.467790828905971,
            #         "addresstype": "tourism",
            #         "name": "National Museum of the American Indian",
            #         "display_name": "National Museum of the American Indian, Maryland Avenue Southwest, Ward 2, Washington, District of Columbia, 20024, United States",
            #         "boundingbox": [
            #             "38.8878653",
            #             "38.8885039",
            #             "-77.0172224",
            #             "-77.0158994",
            #         ],
            #     }
            # ]

            class OSM(TypedDict):
                display_name: str
                """Contains the name and address of the location."""
                lat: float
                """Latitude of the location."""
                lon: float
                """Longitude of the location."""

            def open_street_map(query: str) -> OSM | None:
                """
                Collect address information from Open Street Map.

                Parameters
                ----------
                query : str
                    Anything related to the address / location

                Returns
                -------
                dict | None
                    If no address can be found, None will be returned.
                    If an address is found, a dictionary with the following keys
                    will be returned:
                    - display_name: str; Contains the name and address of the
                      location where key components are split by a comma.
                    - lat: float; Latitude of the location.
                    - lon: float; Longitude of the location.

                """

                print("calling open_street_map", query)
                import requests

                req = requests.get(
                    "https://nominatim.openstreetmap.org/search.php",
                    [
                        ("q", query),
                        ("format", "jsonv2"),
                    ],
                )

                ret = json.loads(req.content)
                print("open_strea_map response", json.dumps(ret, indent=2))
                if len(ret) == 0:
                    return None
                return ret[0]

            chat.register_tool(open_street_map)

            with open(audio_captions_file, "r") as f:
                video_transcript = f.read().replace("\n", " ").strip()

            with open(caption_file, "r") as f:
                post_text = f.read().replace("\n", " ").strip()

            chat_text = f"""video transcript:

            {video_transcript}

            post text:

            {post_text}
            """

            x = chat.chat(chat_text, stream=True, echo="all")
            response_content = (
                x.get_content().removeprefix("```json\n").removesuffix("\n```")
            )
            with open(processed_file, "w") as f:
                f.write(response_content)
            # print(x)

        with open(processed_file, "r") as f:
            post_info = json.load(f)

        lz_file = mp4_file.replace(".mp4", ".json.xz")

        with lzma.open(lz_file, mode="rt") as file:
            lz_json = json.load(file)

            node_info = lz_json["node"]
            instaloader_info = lz_json["instaloader"]
            post_info.update({"node_type": instaloader_info["node_type"]})

            for key in (
                "shortcode",
                "id",
                "__typename",
                "is_video",
                "date",
                "caption",
                "title",
                "viewer_has_liked",
                "edge_media_preview_like",
                "accessibility_caption",
                "comments",
                "display_url",
            ):
                post_info[key] = node_info[key] if key in node_info else None

            owner_info = {
                "owner_id": node_info["owner"]["id"],
                "owner_username": node_info["owner"]["username"],
                "owner_is_private": node_info["owner"]["is_private"],
                "owner_full_name": node_info["owner"]["full_name"],
                # "owner_profile_pic_url_hd": node_info["owner"]["profile_pic_url_hd"],
            }

            post_info.update(owner_info)

        posts.append(post_info)


# gmaps = googlemaps.Client(key="Add Your Key here")

# # Geocoding an address
# geocode_result = gmaps.geocode("1600 Amphitheatre Parkway, Mountain View, CA")
# for post_info in posts:
#     if post_info["latitude"] is None:
#         geocode_result = gmaps.geocode(
#             f"{post_info['street_address']}, {post_info['city']}, {post_info['state']}"
#         )
#         print(geocode_result)
#         post_info["latitude"] = geocode_result["geometry"]["location"]["lat"]


with open(os.path.join(here, "posts.json"), "w") as f:
    json.dump(posts, f, indent=2)

print("\n\nDone!")
