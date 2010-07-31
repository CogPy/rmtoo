

class Config:

    basedir = "tests/blackbox-test/bb003-test/"

    stakeholders = ["executive", ]

    inventors = ["VincentAndJules", "Wulf"]

    reqs_spec = \
        [
           basedir + "input/reqs",
           ["FILES", "FILES"]
        ]

    topic_specs = \
        {
          "ts_common": [basedir + "input/topics", "PulpFiction"],
        }

    analytics_specs = \
        { "stop_on_errors": False,
        }
    
    output_specs = \
        [ 
          ["prios", 
           ["ts_common", basedir + "result_is/reqsprios.tex"]],

          ["graph",
           ["ts_common", basedir + "result_is/req-graph1.dot"]],

          ["graph2",
           ["ts_common", basedir + "result_is/req-graph2.dot"]],

          ["latex2", 
           ["ts_common", basedir + "result_is/reqtopics.tex"]],

          ["html", 
           ["ts_common", 
            basedir + "result_is/html", basedir + "input/header.html",
            basedir + "input/footer.html"]],
        ]
