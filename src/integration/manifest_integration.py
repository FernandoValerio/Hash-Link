class ManifestIntegration:
    def build_manifest(self,builder,acquisition,files):
        return builder.build(acquisition.acquisition_id,acquisition.source_url,acquisition.final_url,acquisition.algorithms,files)
