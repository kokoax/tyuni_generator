f = open("ruby.txt.org")

txt = f.read.split(/\R/).map do |item|
  item.split(/:/)
end
txt = txt.select do |item|
  not item[0].match(/・/) and not item[1].match(/・/)
end

removed = {}
for t in txt do
  removed[t[0]] = t[1]
end

for r in removed.keys() do
  puts(%(#{r}:#{removed[r]}))
end

f.close()
