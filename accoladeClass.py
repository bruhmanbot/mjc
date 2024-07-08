class Acco:
    def __init__(self, acco_name: str, pts: int, double_on_conceal: bool):
        self.acco_name = acco_name
        self.pts = pts
        self.double_on_conceal = double_on_conceal

    def evaluate_score(self, relevant_kans=None, outer_kans=None) -> list:
        # Leave args empty if the concealedness of the kans do not matter
        # Check if all relevantKans are inside Innerkans
        if self.double_on_conceal:
            # If all related kans are inner --> Double score
            try:
                relevant_kans[0]
            except TypeError:
                return [self.pts, self.acco_name]
            for kan in relevant_kans:
                # If one of the related kans is not concealed --> Count normal score
                if kan in outer_kans:
                    return [self.pts, self.acco_name]
            # Next line only executed if all kans are inner i.e. survived for loop above
            return [2 * self.pts, self.acco_name + ' (Concealed)']
        else:
            return [self.pts, self.acco_name]

    def evaluate_score_var2(self, relevant_kans=None, inner_kans=None) -> list:
        # Leave args empty if the concealedness of the kans do not matter
        # Check if all relevantKans are inside Innerkans
        if self.double_on_conceal:
            # If all related kans are inner --> Double score
            try:
                relevant_kans[0]
            except TypeError:
                return [self.pts, self.acco_name]
            for kan in relevant_kans:
                # If one of the related kans is not concealed --> Count normal score
                if kan not in inner_kans:
                    return [self.pts, self.acco_name]
            # Next line only executed if all kans are inner i.e. survived for loop above
            return [2 * self.pts, self.acco_name + ' (Concealed)']
        else:
            return [self.pts, self.acco_name]

    def print_info(self):
        # for debugging
        print(f'{self.acco_name}: {self.pts}, double on conceal: {self.double_on_conceal}')

    def acc_present(self):
        return


if __name__ == '__main__':
    a1 = Acco("Acc1", 1, False)
    a2 = Acco("Acc2", 1, True)

    a1.print_info()
    a2.print_info()

    # Testing for a accolade which doesn't depend on concealed or not
    print(a1.evaluate_score())

    # Testing for inner kan concealed
    print(a2.evaluate_score(relevant_kans=[[1,2,3]], inner_kans=[[1,2,3], [4,5,6]]))
