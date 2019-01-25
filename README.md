Er du også træt af at høre den samme klub 100 igen og igen hver fredag inden du tager i kb? Er din KABS også latterligt langsom til at klistre lydklip sammen i Audacity?

Alle disse problemer og mange flere er nu fortid - saml jeres yndlings YouTube/SoundCloud links i en .csv fil (Google Sheet -> export to csv), og producér en studio quality klub 100 på ~10 minutter.

Brugt til at samle https://soundcloud.com/kenny-olsen/smkid-klub-2-7 af S/M+KID studiestarten '18. ./shoutouts/ og klub.csv brugt til denne klub 2^7 medfølger i dette repo.

# Hvordan, hvor og hvorfor gør jeg ting?

Før du kører noget som helst, bør indholdet af denne mappe have følgende struktur:

```
klub-100-maker/
├── shoutouts/
│   ├── 1.wav
│   ├── 2.wav
│   ├── ...
│   └── n.wav
├── klub.csv
├── dl.py
├── prepare_shoutout.py
├── prepare_track.py
├── prepare_all_shoutouts.py
├── prepare_all_tracks.py
└── combine.py
```

hvor ./shoutouts/n.wav indeholder skud ud'et til den n'te sang i klub 100en, hvis det giver mening. Skud ud'et kommer *før* sangen, så ./shoutouts/1.wav er jeres intro-skud-ud.

## klub.csv

Denne .csv fil indeholder information om sangene i en klub 100. Hver række svarer til en sang og et skud ud, hvor første kolonne er sangens navn, anden kolonne er et YouTube/SoundCloud link, og tredje kolonne er det timestamp (i sekunder) i sangen, hvor jeres ene minut af sangen skal begynde.

## Byg mig en klub 100, tak

* Placér klub.csv i samme mappe som scriptsne
* Kør dl.py for at downloade alle sange til ./tracks/
* Kør prepare_all_tracks.py for at trimme, fade, og loudness normalisere alle sange. Resultatet placeres i ./prepared_tracks/
* Kør prepare_all_shoutouts.py for at loudness normalisere alle skud ud, som ryger i ./prepared_shoutouts
* Kør combine.py for at kombinere sange og skud ud til en endelig klub.mp3.

Kræver:
python3
youtube-dl - for at køre dl.py
ffmpeg - for at køre prepare_track.py, prepare_shoutout.py og combine.py
