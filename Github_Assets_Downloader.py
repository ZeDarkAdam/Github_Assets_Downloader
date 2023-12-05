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
    layout="wide" # wide, centered
)

# hide_st_style = """
#             <style>
#             .stDeployButton {display:none;}
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)



def write_download_page(b_size, name, download_url, download_count, button_type):
    mb_size = bytes_to_megabytes(b_size)
    st.subheader(f'**{name}**')
    st.link_button(f"**Download** ({mb_size} MB)", download_url, help = None, type = button_type, disabled=False, use_container_width=True)
    st.caption(f'Downloaded: **{download_count}** times')




def bytes_to_megabytes(bytes_size):
    megabytes = bytes_size / (1024 ** 2)
    rounded_megabytes = math.ceil(megabytes)
    return rounded_megabytes


def get_github_repo_assets_container(owner, repo_name, extension_filter):

    with st.container(border=True):

        with st.spinner(f'Getting the latest version of {repo_name}...'):
            #time.sleep(0.5)

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

                minutes = time_difference.total_seconds() // 60
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
                elif hours > 0 : 
                    ago = "hours ago"
                    time_num = hours
                elif hours >= 0 : 
                    ago = "minutes ago"
                    time_num = minutes
                ###########################################################################
                
                #with st.container(border=True):
                    
                st.subheader(f"**{repo_name}**\nUpdated **{int(time_num)}** {ago}", divider = 'grey') # 'grey'

                #st.write(f"Updated **{days}** {ago}")
                # st.divider()

                #st.subheader("", divider='gray')


                tab1, tab2 = st.tabs(["Download", f"Changelog"])

                
                with tab1:
                    

                    extension_filter = f".{extension_filter}"
                    
                    # if all_ext == True:   
                    #     extension_filter = ""

                    assets = release_info["assets"] 
                    if assets:
                        for asset in assets:
                            if extension_filter in asset["name"]:
                                
                                write_download_page(asset["size"], asset["name"], asset["browser_download_url"], asset["download_count"], "primary")

                                # mb_size = bytes_to_megabytes(asset["size"])
                                # st.subheader(f'**{asset["name"]}**')
                                # st.link_button(f"**Download** ({mb_size} MB)", asset["browser_download_url"], help = None, type = "primary", disabled=False, use_container_width=True)
                                # st.caption(f'Downloaded: **{asset["download_count"]}** times')



                            elif all_ext:
                                write_download_page(asset["size"], asset["name"], asset["browser_download_url"], asset["download_count"], "secondary")


                    else:
                        st.error("No assets found.")



                with tab2:

                    st.write(release_info["body"])







            else:
                st.error(f"Failed to fetch release information of **{repo_name}**. Status code: [**{response.status_code}**]({repo_url})")

                #st.toast('The request limit from this IP address has been exceeded, please come back later', icon=None)


                error_info = response.json()
                with st.expander("Details", expanded=False) :
                    st.write(error_info["message"])

                return 403



#st.sidebar.title(f'Add repos')
all_ext = st.sidebar.toggle(f'Show all file extensions', value = False)


st.title("Github Assets Downloader")



col1, col2, col3 = st.columns(3)
with col1:
    owner, repo_name, extension_filter = "NoName-exe", "revanced-extended", "apk"
    get_github_repo_assets_container(owner, repo_name, extension_filter)

with col2:
    owner, repo_name, extension_filter = "Team-xManager", "xManager", "apk"
    get_github_repo_assets_container(owner, repo_name, extension_filter)

with col3:
    owner, repo_name, extension_filter = "NeoApplications", "Neo-Store", "apk"
    get_github_repo_assets_container(owner, repo_name, extension_filter)





# st.write("")
# owner, repo_name, extension_filter = "Team-xManager", "xManager", ".apk"
# get_github_repo_assets_container(owner, repo_name, extension_filter)


# st.write("")
# owner, repo_name, extension_filter = "NeoApplications", "Neo-Store", ".apk"
# get_github_repo_assets_container(owner, repo_name, extension_filter)
