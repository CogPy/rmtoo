'''
 rmtoo
   Free and Open Source Requirements Management Tool

 tlp1 output class.

 (c) 2011-2012,2017 by flonatel

 For licensing details see COPYING
'''

from rmtoo.lib.logging import tracer
from rmtoo.lib.StdOutputParams import StdOutputParams
from rmtoo.lib.ExecutorTopicContinuum import ExecutorTopicContinuum
from rmtoo.lib.CreateMakeDependencies import CreateMakeDependencies


class tlp1(StdOutputParams, ExecutorTopicContinuum,
           CreateMakeDependencies):

    class Id2IntMapper:

        def __init__(self):
            self.next_int = 0
            self.mappings = {}
            self.imapping = {}

        def get(self, n):
            if n in self.mappings:
                return self.mappings[n]
            oi = self.next_int
            self.mappings[n] = oi
            self.imapping[oi] = n
            self.next_int += 1
            return oi

    def __init__(self, oconfig):
        '''Create a graph output object.'''
        tracer.debug("Called.")
        StdOutputParams.__init__(self, oconfig)
        CreateMakeDependencies.__init__(self)

    def topic_continuum_sort(self, vcs_commit_ids, topic_sets):
        '''Because tlp1 can only one topic continuum,
           the latest (newest) is used.'''
        return [ topic_sets[vcs_commit_ids[-1].get_commit()] ]

    def requirement_set_pre(self, requirement_set):
        '''This is called in the RequirementSet pre-phase.'''
        with open(self._output_filename, "w") as fd:
            reqs_count = requirement_set.get_requirements_cnt()
            i2im = tlp1.Id2IntMapper()
            self.write_header(fd)
            self.write_node_ids(fd, reqs_count)
            self.write_edges(fd, requirement_set, i2im)
            self.write_labels(fd, i2im)
            self.write_footer(fd)

    # Details
    def write_header(self, fd):
        fd.write('(tlp "2.0"\n')
        # ToDO: very complicated to check this during tests.
        # fd.write('(date "%s")\n' % time.strftime("%d-%m-%Y"))
        fd.write('(comments "This file was generated by rmtoo.")\n')

    def write_node_ids(self, fd, m):
        fd.write("(nodes ")
        for i in range(0, m):
            fd.write("%d " % i)
        fd.write(")\n")

    def write_edges(self, fd, reqset, i2im):
        e = 0
        for rid in sorted(reqset.get_all_requirement_ids()):
            r = reqset.get_requirement(rid)
            ei = i2im.get(r.id)
            for o in sorted(r.incoming, key=lambda t: t.name):
                ej = i2im.get(o.id)
                fd.write("(edge %d %d %d)\n" % (e, ei, ej))
                e += 1

    def write_labels(self, fd, i2im):
        fd.write('(property  0 string "viewLabel"\n')
        fd.write('(default "" "" )')

        for k, v in sorted(i2im.imapping.items()):
            fd.write('(node %d "%s")\n' % (k, v))
        fd.write(")\n")

    def write_footer(self, fd):
        fd.write(")\n")

    def cmad_topic_continuum_pre(self, _):
        '''Write out the one and only dependency to all the requirements.'''
        tracer.debug("Called.")
        CreateMakeDependencies.write_reqs_dep(self._cmad_file,
                                              self._output_filename)
