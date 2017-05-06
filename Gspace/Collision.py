#encoding: utf-8

def collides_with(pos1, size1, pos2, size2):
   return (pos1[0] < pos2[0] + size2[0] and \
           pos1[0] + size1[0] > pos2[0] and \
           pos1[1] < pos2[1] + size2[1] and \
           pos1[1] + size1[1] > pos2[1])