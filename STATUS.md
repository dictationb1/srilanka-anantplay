# Sri Lanka source health

Run timestamp: 2026-11-23T04:41:14+05:30 (Sri Lanka Time, UTC+05:30)

Index: `https://raw.githubusercontent.com/dictationb1/srilanka-anantplay/main/index.json`

- Catalog channels / published site cards: **69 / 69**.
- Published IPTV entries in **each** playlist: **18** across **15** channels.
- Published IPTV manifests verified this run: **10** across **9** channels.
- Primary site HTTP 200 responses: **68/69**; not a live-video playback test.
- Unique probe targets by kind, URL and Referer: **200**.
- Total direct IPTV channels in the **IPTV tab**: **15** (`srilanka_category.m3u` / `srilanka_language.m3u`).
- Total official live TV channels in the **Home / Live Sites tab**: **69** (`srilanka_sites.json`).
- Retained geo-restricted / timeout streams: **7** (listed below).

Safety guard passed: allowed individual HTTP 404/410 or non-HLS exclusions. DNS failures are reviewed, not auto-pruned.

## Retained SL geo-restricted / timeout streams

These curated Sri Lankan feeds resolve, but this probe runner sits outside Sri Lanka (GitHub Actions, US/EU), so they time out, return 403/451, or fail TLS. They are **retained**, labelled `SL Geo-Restricted / Timeout from US Runner (Retained)`, and can play from a Sri Lankan network. They are never a release blocker.

| Channel | Stream | Probed HTTP | Verdict | Curation |
|---|---|---:|---|---|
| Asia TV | `https://stream.asiatvnet.com/1/live/master.m3u8` | — | tls-error | SL Geo-Restricted / Timeout from US Runner (Retained) |
| Charana TV | `https://edge3-moblive.yuppcdn.net/transhd2/smil:chtv05.smil/index.m3u8` | — | timeout | SL Geo-Restricted / Timeout from US Runner (Retained) |
| Shraddha TV | `https://edge3-moblive.yuppcdn.net/drm1/smil:shraddhatvdrm.smil/index.m3u8` | — | timeout | SL Geo-Restricted / Timeout from US Runner (Retained) |
| Star Tamil | `https://edge4-moblive.yuppcdn.net/trans1sd/smil:strtml19.smil/playlist.m3u8?dvr=` | — | timeout | SL Geo-Restricted / Timeout from US Runner (Retained) |
| Swarnavahini | `https://teledrama.ebc.lk/TTT/proxy.php` | 403 | restricted | SL Geo-Restricted / Timeout from US Runner (Retained) |
| The Buddhist TV | `https://edge3-moblive.yuppcdn.net/drm1/smil:thebuddhistdrm.smil/index.m3u8` | — | timeout | SL Geo-Restricted / Timeout from US Runner (Retained) |
| Verbum TV | `https://edge3-moblive.yuppcdn.net/drm1/smil:verbumtvdrm.smil/index.m3u8` | — | timeout | SL Geo-Restricted / Timeout from US Runner (Retained) |

## Suggested primary site swaps

Advisory only: only a confirmed HTTP 403/451/522/525/526 or TLS failure on a primary site is listed, and only when an official mirror answered HTTP 200 to this runner.


| Channel | Retained primary | Primary verdict | Action |
|---|---|---|---|
| Asia TV | `https://stream.asiatvnet.com/` | tls-error | SL Geo-Restricted / Timeout from US Runner (Retained); no verified HTTP 200 alternative exists |

Results reflect the probing network only. HTTP 403/451 can indicate geo or other access restrictions. DNS, TLS and timeout results are not proof of a dead URL. An HLS header does not prove media segments, rights, DRM compatibility or playback. Raw links point to `main`, not the local candidate.

| Target | Attempts | HTTP 200 | HTTP 403/451 | HTTP 404/410 | Other HTTP | No HTTP |
|---|---:|---:|---:|---:|---:|---:|
| raw | 5 | 5 | 0 | 0 | 0 | 0 |
| stream | 21 | 10 | 1 | 1 | 1 | 8 |
| site | 109 | 105 | 3 | 0 | 0 | 1 |
| logo | 65 | 65 | 0 | 0 | 0 | 0 |
| all | 200 | 185 | 4 | 1 | 1 | 9 |

Verdict totals: manifest=10, missing=1, other-http=1, reachable=175, restricted=4, timeout=5, tls-error=4

## All probe results

| Kind | URL | HTTP | Verdict | Detail / playlist action |
|---|---|---:|---|---|
| logo | `https://i.imgur.com/5cyTVRJ.png` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://i.imgur.com/9Zc8G7i.png` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://i.imgur.com/9tODclu.png` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://i.imgur.com/DUzOKWM.png` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://i.imgur.com/J8NA1i9.jpeg` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://i.imgur.com/M66UqPB.png` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://i.imgur.com/RX6IwK8.png` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://i.imgur.com/fjHcr9z.jpg` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://i.imgur.com/sZ3fEMi.png` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/2W9he20iMQKzGqxUL3Q2-zJG9ekLEO7LppkvM0S0DXHVoSHaKQADc9KUgmUUO-IILPduRUXVeQ=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/2ZbQt_SH32MbRjqxfa7nEdcrbSZ-QCIjze1DhL_08vvvy0OSBHRCLpwhJLGOxD87gM3WfUNi6g=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/2bpn6vZ3e0Ufs1fqNZ0Olda-V4ppdDEr6bOxKQglzBhzkopiBg7IK35JcFRr8zP0JR2EsT4B=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/3Esr8U0QZDjmp6BfeaSYmce-njXh6fIMrM0es6uc8m-2VysebPWJohKNHC7Umq-ZvxHT_QBR0A=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/6a8PyIBnnBe1IoNP8DvTxiYHd6EjQ2ezPJ4-8gimTPx3Y2zosTGB_ruQT9K6NimCojz6oYuqxg=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/8F01K-xlE5fsvpYB-GIhmkK2zbbO-TAOwfqtjaDWUYRRgeofAthK9viwaf0auImMBs5R0gKhJQ0=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/AW4eQ488vtUd4O44umhShZn9LaTqG39j6NaNs_hzzJrOyjtApKlh7crzn7kZM-YCOIq2RLQZ6EY=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/BSqzgngL67ou5_puNlYjJ-L2iFZ-_CtTOm0EkUSS97ah4c7QAW_PxajDYMk9_At8pPSABmhSjA=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/E6Ppx6Tm4ZkQplzsQ21Im7AFfxm8rDTbL_jkkGE4Ww8oLsvpnSJiWHoGsCFNq-LfnPORZyb6pg=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/HFZMnMwfpT7mMTWP0jrXn9NFR54_tHkNwqD3HkZkzK21FjlPwyZllkJgDCKE6t2RfKBJDbln1g=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/HwmTMEVoeE7BUrx8ITFMqEHQKn6vvvoVcH7LTs8YZJxceGgr5G1POcGNtxKWH-eowSZ4bRQjhlk=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/N7I0AfjHIioTqjd44Z4YYGtxG0fJd6l6sbNULD8u-i88w_E7GMnh2JLjh37AEBD0I_lb1LeU0Q=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/NBzWhVbBxeTJ8GujjbCdvMRnKX1VAp_dvi2-NDPrLU6tOdXqZ-EU4swoNANwG9_-nh6G_A2Y=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/OgXT-_RPCegRtKZas-n-TEhJ3d-h9LSI-vKQYZu69SQADNM_WmhduUnxfdgZYRXATxw27x_2-g=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/QEXJ2sXA1VTKSZHRl-7o7-ieh9fdNWKDMRS1TeVqfOnRtI-VMUtsziwU2n4yUA-2K6f5IEDZ2Q=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/Qby84iOQX-HUPrUrJDrlRSgezzbR69bmSFb4Ws6VW9VJJUJv9i6d0QYTvDXeDf776avIrE2YHQ=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/SJFZ_j8N51rcsRDlvIfKVxEGy66KtPupJpgziyCPm6GckInXqqoRU8EHbzHrwvsYNh7bXF19=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/Tzpqe9Z9exXR0xWcULWhh_K_AvH7cAKdG3IRCXGfrBoF-oj2KHpc9qU4fI74mvOus2c4aOe-=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/UnizPcs_6aU2SdWJI8gmK-3wO_91WiEqQLonAp3pa6ye3unXTBOhCjMfHfk0UfEbeNtkfJiv=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/XFwaRLH3SoZwZgCQ3VwC1tkK_bpuP3cgmBDr-bVB6z2J3TAT2Klzi4SnF1uB7naAV2mYM6loRQ=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/Xcz0VqIbduEH52GoQSp0KKp5or_lRB6n5uLYI6HkRVR9aXthJGdT2rwrtzVzeUdlX2nwoKaC6yg=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/XssLR9zbs51n-fpDTMM1-WPVI70JwtWzhnTYaIKSvYPb24QbwDpaXEhV7nsZn_uektInMu9y=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/YeCNEep0u7iGqyIzWvTiqZTWny1NvvXY5fqfazlB9n93XvGh_OufnKNU6pR4A1N0EsWfQ8CG=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/cZGa9986DPo60GJtWi4jgo4wn7k0eVURXiTQY9yD8AH6RMR9eT2kaUTBseF0CRi_YDV6T8Gr=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/eqryyxIA9uKct13fkE2SGe0mGysHsufXJMB9mVF5kAQohXa725Mk51nl70ic2avrNBZVz-bACw=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/fBBdjOBHZVGn8mjU9kPMPVo6kAgPhafC-mYQqEbPHn_1RnpKmTqS67c3mR9oqIbs9JmoGz73G90=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/h-DBBjfmZYs2lA04mzko49bDaL8K--9NO93-N4zU0wQ11Ju-LciZHci8eY7aLcggICwNhVVnxg=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/hFLJHfTWEzaLQHijmgImUSmKe8JwegYheWEcvv0w09NG5VOd_FvFWstMsq6BImWhrR7PvLWMF34=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/hnZI8DI6pYFHE_-LlIkZQAMJFJtpS3q3F_jLCrEaeQZhOtyUCO0ICQhgnTm7tWxYVHXbc2VDjA=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/iCs5N08qJLhTPcbDTDGi8-xH-ogFJV0RWBMLzPo_zji6XnnYTPbo2K6Lyhq_9fkUiACT8xkL=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/jpF0RFqbvtus458I7AwYPi76fBx49wZ8i2ta5nse6CpwEQX2JeGtQyTYNeWxBnVsU22bvwhWCQ=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/krdKKbHCJcmCBS-eHNDn9LYF-yRxILw0rkpfyKiDPfMLVMZ4LUzSJ_wBUabhEpuyqKpzraS3Kg=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/m3sHlavbn8IDJNZKGJtl8WpKQ91u5b_rZpUMhe2lQ0F8Py2Ds4mKHBzy5fJlTq9aEnTe61KC09M=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/n2mLeL87UjrGzHwxx9MDeZiFRUUSOeHlvpILuwEJIx-TKWbjJYpthWVC-NVG5bmBKeqhR_tf2qM=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/nWD1WT6UEUvYZBhRdpIv1m_Tstk291ZPTvBPRnxVouT-7A1gHg01LZbWGK45zQYd2YIkYSnXUQ=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/nlV4tpla_16qyXzv5rZ6c1hslJsLQeHGOURC1ZQGvrNA5w1hWZwo5MQn4u8LRdMCI2DCNvExKg=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/os_CkpUDlVN0vXN9_1JKm72MqWhEzZeXUr4O9rTK7t_pBrkzl5RwdlQmltIrtvz3f2OM25liww=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/tvwqvVTCQ32fHF5cxjFwFM1Vp9skbdorL6EA2pwvZnlVaPGfhiC1cV9I6LBAM00i-LOSiCUW0g=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_l1Yu7LHjOLhZr8SwNulFwcZiHBFaJ389uLXBlr6tJvkw=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_l4_qA_8eGcYzFErxa-Bccwixf7jz92mgehiJK_yrg=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_lBG4Q2j7htJbxg-phr_qVcAKlNOGbhJhWBe0SkBAuX3EdiRFA_mJUmpSD86gxTbRG5GQ=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_lVWraBn0a1sEA_1KpW2SM4uJwy_8yOlTYSuYPSgISNHCLQwyyu6T_DJvcGl5Wq2SmwtA=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_ldKo-6CgIIEwFgqgSR1Z2-YZQTmje3nwL1PbJHENeALA=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_lguMLI5sGULE3AfJQU0kaoKON2PPvpCe2ryYugxfwYMg=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_liRwpesvTiLGbUjS0wUkL7lp4MzxV8jK7xsnjw70jcLw=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_lwf9VKpD5PW5_jNX4lRKZePfMrF9oov4SzhTPSxOicG4w=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_lwmWpMXI4zzf-rDWyAaPGDxAHVnmMbsWpXqDklXyaj018=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_m9vnpvLDuCjN3benUeTYbdwWWXR-SG2Q9WZSq15GVI1DuDYBub2lf4hmef0g1yidFIrw=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_mIwmOWixO3beIzPS1KrkOcL7bCtFf4JjSrxK3XBh3w8AGlMUaGWuQGy0UKisQHftHW9Q=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_mP6tO1vNaiDr7Vpu-wyMAvA9kvRGnB_saUP8ihXy8a-FU=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_mQhw2e-8XzIXjUxYc5q7ohhiKqts9EZ1GJFnjHm64HJA=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_mSi5BW_UR2q8H6RFJy5Nwoke9jMicBTlHyByHhyDaAQggqAB1VERuCiB4qTCrFpbzqCw=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_mtFPVVUgycRY_zYdQ5yuj4-tEt4xl0ZhD3S-d88_ZXVA=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_mtbLEtYJ7viUdTt34u08S_Td-T6TrlJ4bj4jOBFl5mkw=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_nQjNKO7Ph75ILx8J9F4YNfOJ3VVf2WlNYl0FOYAt3_nutCiN_c5_w2KHRFi-8WgLsaTw=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| logo | `https://yt3.googleusercontent.com/ytc/AIdro_nkhtRGKnWZXxeRBt3WTxz7DzLVIiPqXyEqIJMkri0=s900-c-k-c0x00ffffff-no-rj` | 200 | reachable | HTTP only; content and playback not verified |
| raw | `https://raw.githubusercontent.com/dictationb1/srilanka-anantplay/main/index.json` | 200 | reachable | HTTP only; content and playback not verified |
| raw | `https://raw.githubusercontent.com/dictationb1/srilanka-anantplay/main/sources.txt` | 200 | reachable | HTTP only; content and playback not verified |
| raw | `https://raw.githubusercontent.com/dictationb1/srilanka-anantplay/main/srilanka_category.m3u` | 200 | reachable | HTTP only; content and playback not verified |
| raw | `https://raw.githubusercontent.com/dictationb1/srilanka-anantplay/main/srilanka_language.m3u` | 200 | reachable | HTTP only; content and playback not verified |
| raw | `https://raw.githubusercontent.com/dictationb1/srilanka-anantplay/main/srilanka_sites.json` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://ahasatv.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://athavantv.com/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://athavantv.com/live/new-stream.php?w=100%25&h=390` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://channeleye.lk/rupavahini-live-webcast/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://dammika.tulix.tv/iframe/plan1-a.php?s=slrc2&c=slrc2` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://gajatv.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://goldfm.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://ibctamil.com/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://itn.lk/live/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://lakhanda.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://lankasri.com/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://live.sirasatv.lk/` | 403 | restricted | possible geo/access restriction; location not inferred |
| site | `https://nethfm.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://nethratv.lk/rupavahini-live-webcast/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://player.twitch.tv/?channel=charanatv_livestream` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://player.twitch.tv/?channel=newsfirstsl` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://rangirisrilanka.lk/tv/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://shakthitv.lk/live/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://sirasafm.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://siyathatv.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://siyathatv.lk/live/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://stream.asiatvnet.com/` | — | tls-error | 3 attempts |
| site | `https://sunfm.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://swarnavahini.lk/` | 403 | restricted | possible geo/access restriction; location not inferred |
| site | `https://talenttv.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://tv.rupavahini.lk/rupavahini-live-webcast` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://tv1.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.adaderana.lk/` | 403 | restricted | possible geo/access restriction; location not inferred |
| site | `https://www.charanatv.lk/watch-live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.derana.lk/live/index.php` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.hirunews.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.hirutv.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.hirutv.lk/hirulive.php` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.jayatv.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.jayatv.lk/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.newsfirst.lk/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.parliament.lk/en/parliament-live/chamber-live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.rupavahini.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.shraddha.lk/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.thepapare.com/live/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.verbumtv.com/` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/@DANNEWSTV/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/@DanChannelsLive` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/@ParliamentofSriLankaOfficial/streams` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/@rupavahiniLiveStream/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC-FHqQjZEz1bKvnU8zAT9kQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC0_tgNvLgTJbcTSpuaQzcPg/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC197_phntGZo8pgFNIW-jUw` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC1CkcuwxCW_dIchuR0tTCJw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC2L1SsEmGrARu0LagZUPukA` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC5II-XiFOAMHfqIcdH3JOXQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC5i6j8XFN-8uUBbu0rCwH4A/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC6YWhRiXB9AXQDcVpPtKslA/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC6b6XrsNOxQiS-FdfE8-Avw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC8AMm5NxsMra2cjlewCb8QA/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC8lKgUHo-2m1z6OoZB9CNmA/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UC98ekB6ciaLZIEee-h93IgQ` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCAfpnYCjpjXUyCG2TzuNmzQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCB5aqOetGShRd8COycdf_PQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCBUl3Q7dwg0nBdwcUA-9qsw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCCiNqOMFZvfLJoUs8qcNWmQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCDR8ZWHRheX5Y1jn5ZS1Vag/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCED67w-HOOpeWoY9vqzgyog/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCEuqtAYLS6nvKLUzQcV7lgA/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCOQM5Fb-JjqM61QqA-nlKCg/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCOoCpNa2WliqrXOcOAMBpBQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCOtYyt7W5PmPnwQjWWF_Z-Q/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCQIRNmBsioZ0MelTT6PfuTg/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCQLv6eVNJPfzw4AHP-2O5wQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCQTcNhAZidy1i9wwmdgf2Lw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCQii5eghTJ5knI1_reM3xvg` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCRyQB76ROvxKbcW4SOTUFcA` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCT5jQx38HY6FVZUkg4XmofA` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCTlpgdx9M7Zi7SNexG2_Gfw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCUs5-PFhqto4TzPC6ykYzIw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCV4GLFGsZIw1bDfqgzlLNeA` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCW_rA_jb-_vbZtU4cTpnT5Q/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCXFcukf9VvSWp731oQDJ7Bg/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCYIPWw_op6ekQQAdlcrYTrA/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCZwrd_UhUk9_JXSC8eMYu9g/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCaI8gOmwQZJpganFN4-SZlg` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCaIc6SgS90ud_RgMSC6hW_w/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCbkMFGQ_RWIxbZt4FsnNhFg/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCc30sTBdN9LRSxEuHaXV_bQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCcDzc3CNB9g096rvxPb5Jdg/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCcK65sl0aZPEUbPmWq5hfNQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCcpIxAzRhFTR2aAZz-wpYng` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCeK7UyzG2P2Rd7Db91dfDEQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCfQqHQ0uiF7OHo6peS-8Rsw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCg2azB8aZfuwJpifS7w9Qow/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCgFK94EtfymL9AvhxQucaTw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCgUD68IjZ2XS0DqfmDuiTsA/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCgj4AYKJHZCFjsG-0YqBbDQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UChDLy_EdNeFmw54sQqWVjfg/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCjhJIuEe5cDuA463WpNsngA/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCjm7vbOwssao7Bhm9wX3-bw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCoQXpCWew0Q3qz6buZYOAFg/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UConsxAXaeWT43x4FNs1nXPA/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCqE4lfEdtS2A0mTsoBkyNpw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCsExZudI-3Bfi2ubAdwcgHw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCu2CZBA74eIFLo5S7dN_1Ww/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCu3vWkFUnfddXnd0tsmmkkQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCuAsZtroEqW5tKYsb4IbpFA` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCuIUjcOHWjdfMFw_YGt8aLQ/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCvQVUmJfQc-ov9cPaRcA3Rw/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCwWwogHe02_iesos_QYyV3A/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCwwBQhIa_bqhjC3OHAFOe-w/live` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCyxbER1SNYJ7ENSdzV1fQ-A` | 200 | reachable | HTTP only; content and playback not verified |
| site | `https://www.youtube.com/channel/UCzbjAV5aqbJ790BcD3LkSJg/live` | 200 | reachable | HTTP only; content and playback not verified |
| stream | `https://183.giatvcdn.com/ssh101/ssh101/imaitv/chunks.m3u8` | 200 | manifest | published |
| stream | `https://ahasatv.lk/live-stream/rewind-3600.m3u8` | 404 | missing | not published |
| stream | `https://cast.talenttv.lk/hls/mcrlo1ygwpu8x4bj/index.m3u8` | 200 | manifest | published |
| stream | `https://edge3-moblive.yuppcdn.net/drm1/smil:shraddhatvdrm.smil/index.m3u8` | — | timeout | 3 attempts; published |
| stream | `https://edge3-moblive.yuppcdn.net/drm1/smil:thebuddhistdrm.smil/index.m3u8` | — | timeout | 3 attempts; published |
| stream | `https://edge3-moblive.yuppcdn.net/drm1/smil:verbumtvdrm.smil/index.m3u8` | — | timeout | 3 attempts; published |
| stream | `https://edge3-moblive.yuppcdn.net/transhd2/smil:chtv05.smil/index.m3u8` | — | timeout | 3 attempts; published |
| stream | `https://edge4-moblive.yuppcdn.net/trans1sd/smil:strtml19.smil/playlist.m3u8?dvr=` | — | timeout | 3 attempts; published |
| stream | `https://g4wlkqqwl23a-hls-live.5centscdn.com/NDTVLANKA/1ff5fa54d14c3ff6c6bd3918bbb7db5d.sdp/playlist.m3u8` | — | tls-error | 3 attempts; not published |
| stream | `https://jalworldiptv.vercel.app/iptv/imaitv/playlist.m3u8` | 429 | other-http | 3 attempts; published |
| stream | `https://jk3lz8xklw79-hls-live.5centscdn.com/lpl/d0dbe915091d400bd8ee7f27f0791303.sdp/playlist.m3u8` | — | tls-error | 3 attempts; not published |
| stream | `https://live.jayatv.lk/hls/stream.m3u8` | 200 | manifest | published |
| stream | `https://mumbai-edge.smartplaytv.in/ShakthiTV/index.m3u8` | 200 | manifest | published |
| stream | `https://oj7lnxonyg82-hls-live.5centscdn.com/uks/24263a839810d2041a349baaeef36a79.sdp/playlist.m3u8` | 200 | manifest | published |
| stream | `https://rpn.bozztv.com/slrclive/slrc/slrclive/index.m3u8` | 200 | manifest | published |
| stream | `https://rpn.tulixcdn.com/slrclive/slrc/slrclive-mobile/index.m3u8` | 200 | manifest | published |
| stream | `https://rtmp01.voaplus.com/hls/6x6ik312qk4grfxocfcv.m3u8` | 200 | manifest | published |
| stream | `https://stream.asiatvnet.com/1/live/master.m3u8` | — | tls-error | 3 attempts; published |
| stream | `https://teledrama.ebc.lk/TTT/proxy.php` | 403 | restricted | possible geo/access restriction; location not inferred; published; Referer `https://swarnavahini.lk/` |
| stream | `https://tv.hiruhost.com:1936/8012/8012/playlist.m3u8` | 200 | manifest | published |
| stream | `https://video-eu1.streamerr.co/hls/scb80244b91/live.m3u8` | 200 | manifest | published |
