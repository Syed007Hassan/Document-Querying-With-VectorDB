class ReorderModel:
    def __init__(self):
        self.reorderData = []
        self.vendorData = []

    def add_reorder_data(self, reorder_data):
        self.reorderData.append(reorder_data)

    def add_vendor_data(self, vendor_data):
        self.vendorData.append(vendor_data)

    def get_reorder_data(self):
        return self.reorderData

    def get_vendor_data(self):
        return self.vendorData
