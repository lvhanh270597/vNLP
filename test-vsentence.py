from data_structures.vsentence import vSentence
from data_structures.vtext import vText, load_data
from data_structures.vword import vWord, load_dawg


# text = vText()
# text.get_from_url("https://matplotlib.org/")
# text.remove_html_tag() 
# print( text.adjust() )

text = vText()
text.get_from_url("http://visoul.me/tien-xu-ly-van-ban-tieng-viet/")
text.remove_html_tag()
print("--") 
print( text.adjust() )
# print("-" * 40)
# # print( text.word_freq() )
# # text.word_plot(top_size=50)
# # sentence = vSentence("Khi một thứ gì đó mất đi, người ta thường chỉ thấy được sự mất mát.")

# # text.char_plot(top_size=50)
# # print( text.tokenize() )
# # print( text.separate() )
# print ( text.remove_accents() )
# print ( "-" * 80 )
# print ( text.add_accents() )
# print ( "-" * 80 )
# text.remove_accents()
# print ( text.add_my_accents("/home/hanhlv/tools/system/vdata/dataset.txt", 'text') )
# print(text.get_words_function(lambda x : len(x) == 2))

# print ( text.translate() )

text_replaces = [
    (
        r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
        ""
    ),
    (
        r"\(.*?\)",
        ""
    ),
    (
        r"\{.*?\}",
        ""
    ),
    (
        r"From:(.*?)Sent:(.*?)Cc:(.*?)Subject: (Re\: FW\:)?",
        ""
    ),
    (
        r"\w+([a-z0-9]+)?@\w+\.\w+(\.\w+)?",
        ""
    ),
    (
        r"(.*?)\.(.*?)",
        r"\1 . \2"
    ),
    (
        "Subject: Re: FW",
        ""
    ),
    (
        r"[A-Z]\w+\, [A-Z]\w+ \d+\, (at )?\d+\:\d+(\:\d+)? (PM|AM)",
        ""
    ),
    (
        r"[A-Z]\w+\, [A-Z]\w+ \d+\, (at )?\d+ (PM|AM)",
        ""
    ),
    (
        r"[A-Z]\w+\,\s[A-Z]\w+\s\d+\,\s\d+",
        ""
    ),
    (
        r"Thanks(&amp;|amp;)?Regards(\,)?",
        r""
    ),
    (
        "\&[a-z]+\;",
        ""
    ),
    (
        r"\d+\:\d+",
        ""
    ),
    (
        r"(\d+\,)+\d+đ?",
        ""
    ),
    (
        r"\| (.*?) ",
        ""
    ),
    (
        r"\d+\/\d+(\/\d+)?",
        ""
    ),
    (
        r"Addr: (.*?) Vietnam",
        ""
    ),
    (
        r"br\b",
        ""
    ),
    (
        r"(\d+)([a-z]+)",
        r"\1 \2"
    ),
    (
        r"(Mobile\:)?\d+(\.\d+\.\d+)?\b",
        ""
    ),
    (
        r"\s+",
        " "
    ),
    (
        r"\s+(\,|\.)",
        r"\1"
    ),
    (
        r"([\,\.\:])([\,\.\:])",
        r"\1"
    )
]

print( "-" * 80 )


load_data("./vdata/white-list.txt", "./vdata/am-ngu.txt")
last_text, removeWords = text.preprocessing(text_replaces)
print(removeWords)

# load_dawg("./vdata/am-ngu.txt")
# word = vWord("did")
# print( word.get_similarities( maxCost=2 ) )