investor_registration_form = {
  "config": {
    "wide_screen_mode": True
  },
  "elements": [
    {
      "tag": "markdown",
      "content": "**Welcome to VentureBridge Platform**\nYou can choose your industry field of interest in the below form"
    },
    {
      "alt": {
        "content": "",
        "tag": "plain_text"
      },
      "img_key": "img_v3_026i_55d0b2ac-919a-4096-842f-01b9f30cfcah",
      "tag": "img"
    },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "Register"
          },
          "type": "primary",
          "multi_url": {
            "url": "https://df76zxdr2no.sg.larksuite.com/share/base/form/shrlgW1NRd3weUS0aZQ8bKhdUQM",
            "pc_url": "",
            "android_url": "",
            "ios_url": ""
          }
        }
      ]
    }
  ],
  "header": {
    "template": "purple",
    "title": {
      "content": "Investor Registration Card",
      "tag": "plain_text"
    }
  }
}

startup_registration_form = {
  "config": {
    "wide_screen_mode": True
  },
  "elements": [
    {
      "tag": "markdown",
      "content": "**Welcome to VentureBridge Platform**\nPlease fill in your startup information to join us!"
    },
    {
      "alt": {
        "content": "",
        "tag": "plain_text"
      },
      "img_key": "img_v3_026i_55d0b2ac-919a-4096-842f-01b9f30cfcah",
      "tag": "img"
    },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "Register"
          },
          "type": "primary",
          "multi_url": {
            "url": "https://df76zxdr2no.sg.larksuite.com/share/base/form/shrlgQ1GlTuFkT7UUs1dwE9xjrc",
            "pc_url": "",
            "android_url": "",
            "ios_url": ""
          }
        }
      ]
    }
  ],
  "header": {
    "template": "purple",
    "title": {
      "content": "Startup Registration Card",
      "tag": "plain_text"
    }
  }
}

startup_new_docs_template = {
    "title": {
        "elements":[
            {
                "type": "textRun",
                "textRun":{
                    "text": "Startup Pitching Document - {startup_name}",
                    "style": {}
                }
            }
        ]
    },
    "body": {
        "blocks":[
            {
                "type": "paragraph",
                "paragraph": {
                    "elements":[
                        {
                            "type": "textRun",
                            "textRun": { 
                                "text": "Congratulations, you have successfully join our VentureBridge community! You can use this docs to introduce your startup.",
                                "style": {}
                            }
                        }
                    ]
                }
            },
        ]
    },
}

def get_docs_redirection_form(docs_url):
    return {
      "config": {
        "wide_screen_mode": True
      },
      "elements": [
        {
          "tag": "markdown",
          "content": "**Thanks for being a part of VentureBridge Platform**\nYou can create on the button below to create a pitching document to give the investor a big picture to your business :)"
        },
        {
          "tag": "action",
          "actions": [
            {
              "tag": "button",
              "text": {
                "tag": "plain_text",
                "content": "Create"
              },
              "type": "primary",
              "multi_url": {
                "url": docs_url,
                "pc_url": "",
                "android_url": "",
                "ios_url": ""
              }
            }
          ]
        }
      ],
      "header": {
        "template": "purple",
        "title": {
          "content": "Time to Introduce Your Business!",
          "tag": "plain_text"
        }
      }
    }