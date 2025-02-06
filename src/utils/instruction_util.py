import os
import random
from . import file_util
def get_instruction_list(language_type='zh'):
    """获取对应的指令列表
    参数：
        language_type (str): 语言类型 ('zh' 或 'en')
    返回:
        无
    """
    file_path='data/instruction/zh.json'
    if language_type == 'en':
       file_path='data/instruction/en.json'
    assert(os.path.exists(file_path),f"[get_instruction_list]:{file_path} is not exist")
    ok,instruction=file_util.read_json_from_file(file_path)
    if not ok:
        raise ValueError(f"[get_instruction_list]:{file_path} read_json_from_file not ok")
    return instruction

class instruction_build_util:
    def __init__(self,language_type='zh'):
        self.instruction_list = get_instruction_list(language_type)
        self.instruction_map = {
            instruction['id']: instruction for instruction in self.instruction_list
        }
        self.type_dependency_dict = {
            "global": [],
            "structural control": ["global"],
            "variable": ["global", "structural control"],
            "interface": ["global", "structural control"],
            "function":["global", "structural control"],
            "class": ["global", "structural control"],
            "file": ["global", "structural control"],
            "combination": ["variable", "interface", "class", "file","function"]
        }
        self.contradiction_list=[
            [3,4],
            [8,9],
            [10,11],
            [12,13],
            [14,15],
            [16,17],
            [18,19],
            [24,25],
            [27,28],
            [24,4]
        ]
        self.id_dependency_dict={
            48:[36],
            47:[36,34],
            46:[29],
            45:[29],
            44:[34],
            43:[34],
            42:[34,32],
            41:[32],
            40:[34],
            38:[37],
            35:[34],
            33:[32],
            30:[29],
            28:[20],
            27:[20],
            26:[20],
            25:[20],
            24:[20],
            23:[20],
            22:[20],
            26:[20],
            23:[20],
            25:[20],
        }
    def get_format_keys(self,instruction_id_list):
        """获取指令id对应的参数列表
        参数：
            instruction_id_list (list): 指令id列表
        返回:
            list: 参数列表
        """
        format_keys = []
        for instruction_id in instruction_id_list:
            if instruction_id not in self.instruction_map:
                raise ValueError(f"No instruction with ID {instruction_id}")
            format_keys.extend(self.instruction_map[instruction_id]['format_keys'])
        format_keys = list(set(format_keys))
        return format_keys
    def get_random_instruction_id_list(self,num):
        # Extracting ids from instruction list
        id_list = [instruction['id'] for instruction in self.instruction_list]
        
        if 1 not in id_list:
            raise ValueError("'1' is not in the instruction list")

        # We proceed by first including '1' in our chosen_ids
        chosen_ids = [1]
        
        # We remove '1' from id_list and prepare to pick remaining ids
        id_list.remove(1)
        
        while len(chosen_ids) < num:
            temp_id = random.choice(id_list)
            
            # Check if this id contradicts with any group of ids in chosen_ids
            conflict = any(set(ids).issubset(chosen_ids + [temp_id]) for ids in self.contradiction_list)
            if not conflict:
                chosen_ids.append(temp_id)
                id_list.remove(temp_id)
        for id in chosen_ids:
            if id in self.id_dependency_dict:
                chosen_ids.extend(self.id_dependency_dict[id])
        chosen_ids=list(set(chosen_ids))
        chosen_ids=sorted(chosen_ids)
        return chosen_ids
    def build_instruction_list(self,instruction_id_list,kwargs):
        """构建提示列表。
        参数：
            instruction_id_list (list): 指令id列表
            kwargs (dict): 参数
        返回:
            list: 构建的提示列表。
        """
        instruction_list=[]
        for instruction_id in instruction_id_list:
            instruction_list.append(self.build_instruction(instruction_id,kwargs))
        return instruction_list
    def build_instruction(self,instruction_id,kwargs):
        """构建提示。
        参数：
            instruction_id (int): 指令id
            kwargs (dict): 参数
        返回:
            str: 构建的提示。
        """
        instruction=self.instruction_map[instruction_id]
        # 使用格式化字符串构建指令，kwargs中的键值将替换掉模板字符串中的关键词
        result = instruction['instruction_format'].format(**kwargs)
        return result
    
    def build_dependence(self, instruction_id_list):
        dependence_map = {}
        for instruction_id in instruction_id_list:
            if instruction_id not in self.id_dependency_dict:
                continue
            dependencies = []
            if instruction_id not in self.instruction_map:
                raise ValueError(f"No instruction with ID {instruction_id}")
            try:
                for other_instruction_id in instruction_id_list:
                    if other_instruction_id != instruction_id:
                        if other_instruction_id in self.id_dependency_dict[instruction_id]:
                            dependencies.append(other_instruction_id)
                        elif self.instruction_map[other_instruction_id]['type']=='global':
                            dependencies.append(other_instruction_id)
                dependence_map[instruction_id] = dependencies
            except KeyError as e:
                print(f"KeyError for instruction ID {instruction_id} with type causing error: {e}")
        return dependence_map

