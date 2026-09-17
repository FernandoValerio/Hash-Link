class ManifestValidator:
    REQUIRED=("acquisition_id","source_url","files")

    def validate(self, manifest:dict)->bool:
        return all(field in manifest for field in self.REQUIRED)
