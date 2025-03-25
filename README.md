# SwitchScraperV4

## Previous Shenanigans
- V1, It was kinda working but it had issues with adding things to it because it was flex taped together.
- V2, I tried to refactor whole V1 but i rewrote how i handle data, Including one SSH session to try all authentication attempts. It had weird issues when switch was thinking for too long. When it worked it was blazingly fast but was undebuggable.
- V3, Was a rewrite to Java under this repo https://github.com/MateuszSerafin/JswitchLib, TLDR; Unnecessarily complicated. Wanted better support to handle concurrent connections, parsing was painful.
- V4, This time I got it, The new approach is to Keep It Simple Stupid, While commiting Authentication (Tested) has around 200 lines of code. It will be slower but if it works it works.
- I also tried Ansible, the problem is Telnet not supported. I would need to handle it really specifically and in weird manner to work especially with multiple vendors. Would be overcomplicated. I just need to login do commands parse done. Also, not all vendors have a good support. TLDR; Ansible? Well yes but actually no
- NetMiko doesn't support nested ssh, any way would require doing authentication via my api
- ssh user@ip command doesn't work on switches (or at least on all of them)
- No using ssh port forwarding wouldn't work in my case

<br>This is the best implementation I could do for my use case 

## Currently
- Be able to theoretically have infinite jump hosts 
- Be able to run it from local machine
    - For now this is not implemented work around is to use local machine with ssh server (Good enough for my case)
- Properly Implemented SSH,Telnet authentication API 
    - Tested on Cisco Only
    - I don't remember if some vendors for telnet did not require to press any key to continue, it will cause issues now but is simple to change, need to test it.
- Execute Commands Per Vendor (TODO)
- Parse the data (TODO)
- Spit out CSV (TODO)

