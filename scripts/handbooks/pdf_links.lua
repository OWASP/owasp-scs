-- Rewrite web-edition Markdown links for the combined PDF document.
--
-- The handbook sources are separate MkDocs pages. When Pandoc combines them,
-- leaving a target such as `part2-foo.md#section` untouched causes WeasyPrint
-- to resolve it against the local build directory and emit a file:/// URI in
-- the PDF. Same-handbook section links become internal PDF destinations;
-- links that need a web page become canonical scs.owasp.org URLs.

local function metadata_string(metadata, key)
  local value = metadata[key]
  if value == nil then
    return ""
  end
  return pandoc.utils.stringify(value)
end

local function page_url(site_base, book_slug, page_name)
  if page_name == "index" then
    return site_base .. "/" .. book_slug .. "/"
  end
  return site_base .. "/" .. book_slug .. "/" .. page_name .. "/"
end

local function pandoc_fragment(markdown_fragment)
  -- MkDocs retains the numeric section prefix in generated anchors (for
  -- example, #20-appendix-b), while Pandoc's auto_identifier algorithm drops
  -- the leading section number (#appendix-b). The PDF contains Pandoc IDs.
  return markdown_fragment:gsub("^#%d+%-", "#")
end

function Pandoc(document)
  local book_slug = metadata_string(document.meta, "handbook-slug")
  local site_base = metadata_string(document.meta, "handbook-site-base")
  site_base = site_base:gsub("/+$", "")

  if book_slug == "" then
    error("pdf_links.lua: handbook-slug metadata is required")
  end
  if not site_base:match("^https://") then
    error("pdf_links.lua: handbook-site-base must be an absolute https:// URL")
  end

  local site_origin = site_base:match("^(https://[^/]+)")

  local function rewrite_link(link)
    local target = link.target

    if target == "" or target:match("^#") then
      return nil
    end

    -- Keep already absolute links. Normalize protocol-relative links so they
    -- cannot inherit a file: base URL from the PDF engine.
    if target:match("^//") then
      link.target = "https:" .. target
      return link
    end
    if target:match("^[A-Za-z][A-Za-z0-9+%.%-]*:") then
      return nil
    end
    if target:match("^/") then
      link.target = site_origin .. target
      return link
    end

    local path, fragment = target:match("^([^#]*)(#.*)$")
    if path == nil then
      path = target
      fragment = ""
    end

    -- All part files and the bibliography are concatenated into this PDF, so
    -- an anchored same-book link should stay inside the document.
    if fragment ~= "" and
       (path:match("^part[^/]*%.md$") or path == "references.md") then
      link.target = pandoc_fragment(fragment)
      return link
    end

    local destination = nil

    if path == "index.md" then
      destination = page_url(site_base, book_slug, "index")
    elseif path == "../index.md" then
      destination = site_base .. "/"
    else
      local other_book, other_page = path:match("^%.%./([^/]+)/([^/]+)%.md$")
      if other_book ~= nil then
        destination = page_url(site_base, other_book, other_page)
      else
        local same_book_page = path:match("^([^/]+)%.md$")
        if same_book_page ~= nil then
          destination = page_url(site_base, book_slug, same_book_page)
        end
      end
    end

    if destination == nil then
      error(
        "pdf_links.lua: unresolved relative hyperlink in " ..
        book_slug .. ": " .. target
      )
    end

    link.target = destination .. fragment
    return link
  end

  return document:walk({ Link = rewrite_link })
end
