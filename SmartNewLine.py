import sublime, sublime_plugin

class SmartNewLineCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    # TODO: move to settings file
    lines_considered = 2

    for region in self.view.sel():
      # Move to EOL so that the cursor ends on the line I create at the end
      self.view.run_command("move_to", {"to": "eol"})

      # Get the last N lines (N=3 for now)
      (row, col) = self.view.rowcol(region.a)
      prev_lines = []
      for i in range(lines_considered):
        point = self.view.text_point(row-i,0)
        l = self.view.line(point)
        prev_lines.append(self.view.substr(l))
        print(prev_lines[i])
      # Another way to check...
      line_iter = [self.view.text_point(row-i,0) for i in
                    range(lines_considered)]

      # Diff the lines to determine the new prefix
      prefix = ''
      prefix2 = ''
      for i in range(min([len(s) for s in prev_lines])):
        if all([s[i] == prev_lines[0][i] for s in prev_lines]):
          prefix += prev_lines[0][i]
          # print("New prefix: ",prefix)
        else:
          break

      done = False
      while not done:
        print(line_iter)
        token_regions = [sublime.Region(pt,
                         self.view.find_by_class(pt, True,
                                              sublime.CLASS_PUNCTUATION_START |
                                              sublime.CLASS_PUNCTUATION_END |
                                              sublime.CLASS_WORD_START |
                                              sublime.CLASS_WORD_END |
                                              sublime.CLASS_SUB_WORD_START |
                                              sublime.CLASS_SUB_WORD_END ))
                         for pt in line_iter]
        print(token_regions)
        tokens = [self.view.substr(r) for r in token_regions]
        print(tokens)
        if all([s == tokens[0] for s in tokens]):
          prefix2 += tokens[0]
          print("New prefix2: ",prefix2)
        else:
          done = True

        line_iter = [r.end() for r in token_regions]
        if any([self.view.classify(pt) & sublime.CLASS_LINE_END
                  for pt in line_iter]):
          done = True

      # Insert the prefix
      self.view.insert(edit, self.view.line(region).end(), "\n" + prefix2)