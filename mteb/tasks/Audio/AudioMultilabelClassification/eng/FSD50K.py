from __future__ import annotations

import ast
import re

from mteb.abstasks.Audio.AbsTaskAudioMultilabelClassification import (
    AbsTaskAudioMultilabelClassification,
)
from mteb.abstasks.TaskMetadata import TaskMetadata
import datasets

# Check if reverse mapping from MIDS to class labels is needed
# FSD50K_CLASS_LABELS = [
#     "Accelerating and revving and vroom",
#     "Accordion",
#     "Acoustic guitar",
#     "Aircraft",
#     "Alarm",
#     "Animal",
#     "Applause",
#     "Bark",
#     "Bass drum",
#     "Bass guitar",
#     "Bathtub (filling or washing)",
#     "Bell",
#     "Bicycle",
#     "Bicycle bell",
#     "Bird",
#     "Bird vocalization and bird call and bird song",
#     "Boat and Water vehicle",
#     "Boiling",
#     "Boom",
#     "Bowed string instrument",
#     "Brass instrument",
#     "Breathing",
#     "Burping and eructation",
#     "Bus",
#     "Buzz",
#     "Camera",
#     "Car",
#     "Car passing by",
#     "Cat",
#     "Chatter",
#     "Cheering",
#     "Chewing and mastication",
#     "Chicken and rooster",
#     "Child speech and kid speaking",
#     "Chime",
#     "Chink and clink",
#     "Chirp and tweet",
#     "Chuckle and chortle",
#     "Church bell",
#     "Clapping",
#     "Clock",
#     "Coin (dropping)",
#     "Computer keyboard",
#     "Conversation",
#     "Cough",
#     "Cowbell",
#     "Crack",
#     "Crackle",
#     "Crash cymbal",
#     "Cricket",
#     "Crow",
#     "Crowd",
#     "Crumpling and crinkling",
#     "Crushing",
#     "Crying and sobbing",
#     "Cupboard open or close",
#     "Cutlery and silverware",
#     "Cymbal",
#     "Dishes and pots and pans",
#     "Dog",
#     "Domestic animals and pets",
#     "Domestic sounds and home sounds",
#     "Door",
#     "Doorbell",
#     "Drawer open or close",
#     "Drill",
#     "Drip",
#     "Drum",
#     "Drum kit",
#     "Electric guitar",
#     "Engine",
#     "Engine starting",
#     "Explosion",
#     "Fart",
#     "Female singing",
#     "Female speech and woman speaking",
#     "Fill (with liquid)",
#     "Finger snapping",
#     "Fire",
#     "Fireworks",
#     "Fixed-wing aircraft and airplane",
#     "Fowl",
#     "Frog",
#     "Frying (food)",
#     "Gasp",
#     "Giggle",
#     "Glass",
#     "Glockenspiel",
#     "Gong",
#     "Growling",
#     "Guitar",
#     "Gull and seagull",
#     "Gunshot and gunfire",
#     "Gurgling",
#     "Hammer",
#     "Hands",
#     "Harmonica",
#     "Harp",
#     "Hi-hat",
#     "Hiss",
#     "Human group actions",
#     "Human voice",
#     "Idling",
#     "Insect",
#     "Keyboard (musical)",
#     "Keys jangling",
#     "Knock",
#     "Laughter",
#     "Liquid",
#     "Livestock and farm animals and working animals",
#     "Male singing",
#     "Male speech and man speaking",
#     "Mallet percussion",
#     "Marimba and xylophone",
#     "Mechanical fan",
#     "Mechanisms",
#     "Meow",
#     "Microwave oven",
#     "Motor vehicle (road)",
#     "Motorcycle",
#     "Music",
#     "Musical instrument",
#     "Ocean",
#     "Organ",
#     "Packing tape and duct tape",
#     "Percussion",
#     "Piano",
#     "Plucked string instrument",
#     "Pour",
#     "Power tool",
#     "Printer",
#     "Purr",
#     "Race car and auto racing",
#     "Rail transport",
#     "Rain",
#     "Raindrop",
#     "Ratchet and pawl",
#     "Rattle",
#     "Rattle (instrument)",
#     "Respiratory sounds",
#     "Ringtone",
#     "Run",
#     "Sawing",
#     "Scissors",
#     "Scratching (performance technique)",
#     "Screaming",
#     "Screech",
#     "Shatter",
#     "Shout",
#     "Sigh",
#     "Singing",
#     "Sink (filling or washing)",
#     "Siren",
#     "Skateboard",
#     "Slam",
#     "Sliding door",
#     "Snare drum",
#     "Sneeze",
#     "Speech",
#     "Speech synthesizer",
#     "Splash and splatter",
#     "Squeak",
#     "Stream",
#     "Strum",
#     "Subway and metro and underground",
#     "Tabla",
#     "Tambourine",
#     "Tap",
#     "Tearing",
#     "Telephone",
#     "Thump and thud",
#     "Thunder",
#     "Thunderstorm",
#     "Tick",
#     "Tick-tock",
#     "Toilet flush",
#     "Tools",
#     "Traffic noise and roadway noise",
#     "Train",
#     "Trickle and dribble",
#     "Truck",
#     "Trumpet",
#     "Typewriter",
#     "Typing",
#     "Vehicle",
#     "Vehicle horn and car horn and honking",
#     "Walk and footsteps",
#     "Water",
#     "Water tap and faucet",
#     "Waves and surf",
#     "Whispering",
#     "Whoosh and swoosh and swish",
#     "Wild animals",
#     "Wind",
#     "Wind chime",
#     "Wind instrument and woodwind instrument",
#     "Wood",
#     "Writing",
#     "Yell",
#     "Zipper (clothing)",
# ]

class FSD50KClassification(AbsTaskAudioMultilabelClassification):
    # hf_subsets = ["curated", "noisy"]

    # overriding the dataset transform
    # FSD50K dataset labels are not exactly in the format we would like
    # "The sound of [class 1], [class 2], .."" -> [<class 1>, <class 2>, ...]
    # def dataset_transform(self):
    #     def update_class_labels(datapoint):
            # string = datapoint["raw_text"][-1]
            # # "Mids(class_label_id): ['/m/04szw', '/m/085jw', '/m/0l14j_', '/m/04rlf']"

            # els = string.split('[')[-1].split(']')[0]
            # # print(els)

            # els_ = els.split(',')
            # # print(els_)

            # final = [e.strip().strip("'") for e in els_]
            # print(final)


            # m_ids = None
            # for element in datapoint["raw_text"]:
            #     if element.startswith("Mids"):
            #         match = re.search(r"\[.*\]", element)
            #         if match:
            #             m_ids = ast.literal_eval(match.group())
            #             break
            # if m_ids is None:
            #     raise ValueError("unable to find class ids for datapoint")
            # datapoint["text"] = m_ids
            # return datapoint

        # self.dataset = self.dataset.map(update_class_labels)
        # print("train el:", self.dataset["train"][0])
        # print("test el:", self.dataset["test"][0])

    metadata = TaskMetadata(
        name="FSD50K",
        description="Multilabel Audio Classification.",
        reference="https://huggingface.co/datasets/confit/fsdkaggle2019-parquet",  # "https://huggingface.co/datasets/CLAPv2/FSD50K",
        dataset={
            "path": "confit/fsdkaggle2019-parquet", # "CLAPv2/FSD50K",
            "revision": "648a5925c8013e345ae5d36bdda220b1d4b07f24"  # "2facd8adf41307d66592cd71fe4f157fcfdeaff5",
        },  # this is actually used to download the data
        type="AudioMultilabelClassification",
        category="a2t",
        eval_splits=["test"],
        eval_langs={"curated": ["eng-Latn"], "noisy": ["eng-Latn"]},
        main_score="mAP",
        date=(
            "2022-05-06",
            "2022-05-06",
        ),  # Estimated date when this dataset was committed, what should be the second tuple?
        domains=["Web"],  # obtained from Freesound - online collaborative platform
        task_subtypes=["Environment Sound Classification"],
        license="cc-by-4.0",
        annotations_creators="human-annotated",
        dialect=[],
        modalities=["audio"],
        sample_creation="found",
        bibtex_citation=""" @misc{fonseca2022fsd50kopendatasethumanlabeled,
            title={FSD50K: An Open Dataset of Human-Labeled Sound Events}, 
            author={Eduardo Fonseca and Xavier Favory and Jordi Pons and Frederic Font and Xavier Serra},
            year={2022},
            eprint={2010.00475},
            archivePrefix={arXiv},
            primaryClass={cs.SD},
            url={https://arxiv.org/abs/2010.00475}, 
        }
        """,
        descriptive_stats={
            "n_samples": {"test": 10231},
        }
    )

    audio_column_name: str = "audio"
    label_column_name: str = "sound"  # "text"
    samples_per_label: int = 8


    def load_data(self, **kwargs):
        """Load dataset from HuggingFace hub and convert it to the standard format."""
        if self.data_loaded:
            return

        self.dataset = {}
        print(self.hf_subsets)
        self.hf_subsets = ["curated", "noisy"]
        for lang in self.hf_subsets:
            self.dataset[lang] = datasets.load_dataset(name=lang, **self.metadata_dict["dataset"])

        self.dataset_transform()
        self.data_loaded = True
