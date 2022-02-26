
该项目是一个ui自动化黑盒测试的脚本项目。

编写的 python 版本 3.10.1

需要安装的 python 包：

>pip install pyautogui==0.9.50

>pip install opencv-python

>pip install keyboard

WPF可视化工具环境：.net core 3.1

## 使用说明
### 核心原理
通过 doAutomatedText.py 脚本，读取 xml 文件中的配置项，进行自动化测试。

### 可配置项
Session：代表一个会话，一个会话中有多个步骤（StepAction）

--|StepAction: 一个执行步骤，或者说是一个操作，可以是一次鼠标点击，也可以是一次键盘事件，有个参数 StepNumber 来描述唯一性。如果 StepNumber 重复了，在循环中会比较致命。

----|Location: 可选 "absolute" 或 "visualization"，如果值为 "absolute"，则 LocationXY 必填，值为坐标。如果值为 "visualization"，则 VisualImagePath 必填，值为图片地址。

----|LocationXY: Location 选择 "absolute" 的话必填，格式为 x,y 。

----|VisualImagePath: Lacation 选择 "visualization" 的话必填，为脚本的相对路径或绝对路径。

----|Duration: 每个事件执行后停止的时间，单位是 s 。

----|Action: 事件，属性 type 是事件类型，当前可选 "left_mouse_click", "right_mouse_click", "mouse_move", "key_down", "loop"。属性 param 对应不同的 type 有所区别。文字属性一般为事件的描述，但如果在 type = "loop" 的时候，需要改为内容属性，由 StepAction 列表填充。

------|type = "left_mouse_click" || "right_mouse_click" 的时候，param 值为数字，表示用对应的鼠标键点击几次。

------|type = "mouse_move" 的时候，param 为位置信息，格式为 x,y , 表示鼠标移动到某处。

------|type = "key_down" 的时候，param 为具体键值。需要参考 pyautogui.KEYBOARD_KEYS 里进行赋值。

------|type = "loop" 的时候，表示开始循环事件，需要额外对三个属性赋值。循环体由三部分组成，开始不变的部分，结尾不变的部分，中间变化的部分。loopBegin 指代开始不变的部分，可为""（但必须要有这个属性）, 格式为 `"int,...,int"` , loopEnd 指代结尾不变的部分，格式同 loopBegin。vars 指代中间变化的部分，格式为 `"int,...,int;...;int,...,int"`, 分号分割一次循环，逗号分割每次循环需要走的变化部分的方法。

> 举个栗子 <br>
这段 Action 的执行顺序为 3 -> 4 -> 6 -> 5 -> 3 -> 4 -> 7 -> 5 -> 3 -> 4 -> 8 -> 9 -> 5
```
  <Action type="loop" loopBegin="3,4" loopEnd="5" vars="6;7;8,9">
      <StepAction StepNumber="3">
        ...
      </StepAction>
      <StepAction StepNumber="4">
        ...
      </StepAction>
      <StepAction StepNumber="5">
        ...
      </StepAction>
      <StepAction StepNumber="6">
        ...
      </StepAction>
      <StepAction StepNumber="7">
       ...
      </StepAction>
      <StepAction StepNumber="8">
        ...
      </StepAction>
      <StepAction StepNumber="9">
       ...
      </StepAction>
    </Action>
```
----|Broke: 预留字段，未来用于校验结果是否和预期一致，进行阻断的判断。

----|ReTry: 预留字段，未来用于判断如果被阻断，是否继续进行接下来的测试。


## 唠叨一会（大概也是使用方式吧）

> “你的电脑也该长大了，要学会自己做测试！”

于是这个项目应运而生。

前面说到，这个项目核心原理是由两部分组成，一部分是数据部分，就是 xml 文件；另一部分是脚本文件。

如果手动写 xml 文件，非常的耗费精力，使用的人或许会想：“我手动测试比这快呢。”。这违背了设计 ~~躺平(划掉)~~ 自动化测试的初衷。

所以引入了一个工具脚本：mhtConvert.py 。如果熟悉 windows 的朋友可能知道，windows 有个工具是 “步骤记录器”，它可以记录你的每一步操作。而解压它保存的 mht 文件，我们会发现其实操作的信息是使用 xml 格式记录的。这就很好办了，写一个脚本把它转成我需要的 xml 格式就好了。于是我写了 mhtConvert.py。

接下来，这个方法也出现了局限。如果我要在之间加一个方法，还是需要做 xml 的编写工作，而且极易搞错。于是我又编写了一个可视化工具：AutoMatedDataModifer 。直接打开可以编写一个新的 xml 文件；如果把已有的 xml 拖到这个 exe 上打开，就可以读取这个 xml 的内容，并进行可视化。修改后可以再次保存为 xml 文件，这个工具可以保证 StepNumber 不重复。不过有个小意外，我忘记了加删除的功能 Orz，问题不大，等下次有空再加吧。这个工具还有个缺陷是不支持编写 loop Action，不过我想聪明的孩子会新建新的 xml ，再复制回原来的 xml。

所以我设计的使用方式是：先打开【步骤记录器】，然后将要测试的部分跑一遍，得到【mht文件】，再使用【mhtConvert.py】脚本转换得到【xml数据文件】，然后使用【AutoMatedDataModifer.exe】对脚本进行一次修改。之后就可以使用了。当然可能还有可以改进的部分，如果有好主意，可以联系我 email: `wxRachel@Outlook.com` 。

 
愿所有测试同事都被温柔以待，快乐工作~
