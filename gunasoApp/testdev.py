import nude
from nude import Nude

print(nude.is_nude('./nude.rb/spec/images/damita.jpg'))

n = Nude('./nude.rb/spec/images/damita.jpg')
n.parse()
print("damita :", n.result, n.inspect())