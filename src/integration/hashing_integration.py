class HashingIntegration:
    def calculate_hashes(self,file_path,algorithms,hasher_function):
        return {alg: hasher_function(file_path,alg) for alg in algorithms}
