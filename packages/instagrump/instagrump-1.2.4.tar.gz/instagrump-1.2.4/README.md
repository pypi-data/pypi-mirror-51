# Instagrump
Just a simple Instagram Public API wrapper. The codes are self-explanatory.

### Example usage
Installing:
```sh
pip3 install instagrump 
```

Importing:
```sh
from instagrump import Profile,  Content 
```

Initialize Profile class:
```sh
profile = Profile('ig_username')
```

Initialize Content class:
```sh
content = Content('url_with_shortcode_from_Profile')
```

Example to get profile contents:
```sh
[Content(i).get_content() for i in Profile('justinbieber').get_posts()]
```
#### Helpful tip
To get all class attribute:
```sh
dir(your_class_here)
```

### Todos

 - Write MORE Documentations
 - Sleep

License
----
MIT

