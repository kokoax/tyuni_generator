require "uri"
require "csv"
require "open-uri"
require "nokogiri"

class Scrapper
  def initialize()
    @base = "https://ncode.syosetu.com/"
    @rd = File.open("ruby.txt.org", "a")
  end

  def get_suburls(html)
    Nokogiri::HTML.parse(html, nil, nil).xpath(%(//dd[@class="subtitle"]/a)).map do |tag|
      URI.join(@base, tag[:href])
    end
  end

  def get_ruby(url)
    sleep(1)
    html = open(url).read
    Nokogiri::HTML.parse(html, nil, nil).xpath(%(//ruby)).map do |tag|
      inner = Nokogiri::HTML.parse(tag.inner_html, nil, nil)
      org = inner.xpath(%(//rb)).inner_html
      rb = inner.xpath(%(//rt)).inner_html
      {org: org, rb: rb}
    end
  end

  def get_recommend(html)
    Nokogiri::HTML.parse(html, nil, nil).xpath(%(//div[@id="recommend"]/div[@class="recommend_novel"]/a)).slice(0,5).map do |tag|
      tag[:href]
    end
  end

  def get_title(html)
    Nokogiri::HTML.parse(html, nil, nil).xpath(%(//div[@id="novel_color"]/p[@class="novel_title"])).inner_html
  end

  def dump_ruby(rb)
    if (not rb[:org].include?(":")) and (not rb[:rb].include?(":"))
      @rd.puts(%(#{rb[:org]}:#{rb[:rb]}))
    end
  end
end

already = []
next_url = ["https://ncode.syosetu.com/n2732ev/"]
scrapper = Scrapper.new()

# 1.times do |_|
while next_url != []
  now_url = next_url.flatten().clone()
  next_url = []
  for url in now_url
    sleep(1)
    html = open(url).read
    title = scrapper.get_title(html)
    if not already.any?(title)
      already.push(scrapper.get_title(html))

      subs = scrapper.get_suburls(html)

      for src in subs
        rubys = scrapper.get_ruby(src)
        for rb in rubys
          scrapper.dump_ruby(rb)
        end
      end

      next_url.concat(scrapper.get_recommend(html))
    end
  end
end
