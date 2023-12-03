import streamlit as st

import requests
import math
from datetime import datetime

import time
# start_time = time.time()
# st.write(f"Execution time: {time.time() - start_time} seconds")


st.set_page_config(
    page_title="GitHub API Test",
    page_icon= "⬇️",
    layout="centered" # wide, centered
)

hide_st_style = """
            <style>
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)



def bytes_to_megabytes(bytes_size):
    megabytes = bytes_size / (1024 ** 2)
    rounded_megabytes = math.ceil(megabytes)
    return rounded_megabytes


def get_github_repo_assets_container(owner, repo_name, extension_filter):

    with st.spinner(f'Getting the latest version of {repo_name}...'):
        time.sleep(0.5)


        repo_url = f"https://api.github.com/repos/{owner}/{repo_name}/releases/latest"
        
        response = requests.get(repo_url, headers={"Accept": "application/vnd.github+json"})

        if response.status_code == 200:
            ###########################################################################
            release_info = response.json()
            #print("From repo:", repo_url)
            #st.write("Release date:", release_info["published_at"])

            ###########################################################################
            release_date= release_info["published_at"]
            release_date_parsed = datetime.strptime(release_date, '%Y-%m-%dT%H:%M:%SZ')
            time_difference = datetime.utcnow() - release_date_parsed

            hours = time_difference.total_seconds() // 3600
            days = time_difference.days
            weeks = math.ceil(time_difference.days / 7)
            months = time_difference.days // 30.44
            
            if months > 0:
                ago = "months ago"
                time_num = months
            elif weeks > 0:
                ago = "weeks ago"
                time_num = weeks
            elif days > 0:
                ago = "days ago"
                time_num = days
            elif hours >= 0 : 
                ago = "hours ago"
                time_num = hours
            ###########################################################################
            
            with st.container(border=True):
                
                st.subheader(f"**{repo_name}**\nUpdated **{int(time_num)}** {ago}", divider='grey')

                #st.subheader(f"**{repo_name}**") # , divider='red'
                #st.write(f"Updated **{days}** {ago}")
                # st.divider()

                #st.subheader("", divider='gray')

                assets = release_info["assets"] 
                if assets:

                    #num = 0
                    for asset in assets:
                        if extension_filter in asset["name"]:
                            
                            # if num != 0 : st.write(" ")
                            # num += 1
                            st.write(" ")
                            mb_size = bytes_to_megabytes(asset["size"])
                            st.success(f'[**{asset["name"]}**]({asset["browser_download_url"]}) ({mb_size} MB)')
                            st.caption(f'Downloaded: **{asset["download_count"]}** times')


                else:
                    st.error("No assets found.")


        else:
            st.error(f"Failed to fetch release information of **{repo_name}**. Status code: [**{response.status_code}**]({repo_url})")
            #st.toast('**Перевищено ліміт запитів з цього іп, зайдіть пізніше**', icon='🚫')





st.title("GitHub API Test")

owner, repo_name, extension_filter = "NoName-exe", "revanced-extended", ".apk"
get_github_repo_assets_container(owner, repo_name, extension_filter)


st.write("")
owner, repo_name, extension_filter = "Team-xManager", "xManager", ".apk"
get_github_repo_assets_container(owner, repo_name, extension_filter)


# st.write("")
# owner, repo_name, extension_filter = "NeoApplications", "Neo-Store", ".apk"
# get_github_repo_assets_container(owner, repo_name, extension_filter)