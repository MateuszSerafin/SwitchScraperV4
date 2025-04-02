# SwitchScraperV4

## Previous Shenanigans
- V1, It was kinda working but it had issues with adding things to it because it was flex taped together.
- V2, I tried to refactor whole V1 but i rewrote how i handle data, Including one SSH session to try all authentication attempts. It had weird issues when switch was thinking for too long. When it worked it was blazingly fast but was undebuggable.
- V3, Was a rewrite to Java under this repo https://github.com/MateuszSerafin/JswitchLib, TLDR; Unnecessarily complicated. Wanted better support to handle concurrent connections, parsing was painful.
- V4, I Discovered netmiko exists lol, additionally i didn't know that there is ntc_templates, and it parses for me pretty much everything

# Currently
I will do some improvements to it but i wanted to write some base which i can build on top of later on if i need it. 

- Basic API exist, should be easy to add other vendors
- For cisco; vlans, descriptions etc works. 
- Tests are added

# TODO
- Jump gateway (Might not be done)
- Make LAG interfaces somehow integrate to my code because I forgot about it
- Add aruba device as it works with GNS3
- Make a csv export of multiple switches