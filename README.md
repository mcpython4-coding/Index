# Index
These Repo contains index files which give programms like the launcher informations about in what state the game is

How is the information formatted?
there is an core.json file in this project which contains the following data structure:
<version name> -> {

"url": url,  // may be null if not provided 

"stable": stable,

"main": main  // where to launch from

}
