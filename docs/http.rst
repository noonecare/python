* tunnel

    #. fiddler 能解码 tunnel 中的消息吗？

        下面这段话，摘自《http 权威指南》::

            Because the tunneled data is opaque to the gateway, the gateway cannot make any
            assumptions about the order and flow of packets. Once the tunnel is established,
            data is free to flow in any direction at any time.

        按这段话的说法，proxy 没法查看 tunnel 中的数据。proxy 能够看到 tunnel 中的所有 packet, 但是 proxy 没法拼接，解码出来
        这些信息。

        我发现，使用 fiddler 可以解码 https tunnel 中的消息。我抓取了如下消息，说明 fiddler 可以抓取 https tunnel 中的消息。

        Fiddler 能不能解码 tunnel 中走其他协议的 TCP 消息，尚未可知。

        .. code-block::

            HTTP/1.1 200 Connection Established
            FiddlerGateway: Direct
            StartTime: 11:17:39.311
            Connection: close

            Encrypted HTTPS traffic flows through this CONNECT tunnel. HTTPS Decryption is enabled in Fiddler, so decrypted sessions running in this tunnel will be shown in the Web Sessions list.

            Secure Protocol: Tls12
            Cipher: Aes128 128bits
            Hash Algorithm: Sha256 256bits
            Key Exchange: RsaKeyX 2048bits

            == Server Certificate ==========
            [Subject]
              CN=*.jd.com, O="BEIJING JINGDONG SHANGKE INFORMATION TECHNOLOGY CO., LTD.", L=beijing, S=beijing, C=CN

            [Issuer]
              CN=GlobalSign Organization Validation CA - SHA256 - G2, O=GlobalSign nv-sa, C=BE

            [Serial Number]
              3A755F6565BC2363315084FF

            [Not Before]
              2017/12/29 12:52:02

            [Not After]
              2018/8/28 17:42:54

            [Thumbprint]
              91D298115B56679EBA1ECD38CDFA0368388970C2

            [SubjectAltNames]
            *.jd.com, *.3.cn, *.360buy.com, *.360buyimg.com, *.7fresh.com, *.baitiao.com, *.caiyu.com, *.chinabank.com.cn, *.jd.co.th, *.jd.hk, *.jd.id, *.jd.ru, *.jdpay.com, *.jdx.com, *.joybuy.com, *.joybuy.es, *.jr.jd.com, *.kmall.jd.com, *.m.jd.com, *.m.paipai.com, *.m.yhd.com, *.paipai.com, *.toplife.com, *.wangyin.com, *.yhd.com, *.yihaodianimg.com, *.yiyaojd.com, 3.cn, 360buy.com, 360buyimg.com, 7fresh.com, baitiao.com, caiyu.com, chinabank.com.cn, jd.co.th, jd.hk, jd.id, jd.ru, jdpay.com, jdx.com, joybuy.com, joybuy.es, paipai.com, toplife.com, wangyin.com, yhd.com, yihaodianimg.com, yiyaojd.com, jd.com


    #. 如果 tunnel 是为了与 non-http server 连接，那么为什么非要走 http 的 connect 请求?

    #.

* TCP 三次握手，四次挥手。


* TCP 重发机制。

* 走 TCP 协议的




