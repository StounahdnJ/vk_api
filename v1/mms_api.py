class mms:
    data=[{"id":"","text":""}]
    def mms_add(self,id,text):
        mn=0
        sex=0
        for line in self.data:
            if line['id']==id:
                self.data[sex]['text']=text
                mn+=1
            sex+=1
        if mn==0:
            self.data.append({"id": id, "text": text})
        print(1)
    def mms_search(self,id):
        for line in self.data:
            if line['id']==id:
                return line['text']