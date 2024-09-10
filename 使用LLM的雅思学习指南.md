# 使用LLM的雅思学习指南

## 写在前面

准备考雅思，尝试使用chatGPT这样子的LLM辅助我学习。但是我在网上搜索了一下，没有多少关于这方面优秀的prompts

下面这个，来自于awsome-

> 我希望你假定自己是雅思写作考官，根据雅思评判标准，按我给你的雅思考题和对应答案给我评分，并且按照雅思写作评分细则给出打分依据。此外，请给我详细的修改意见并写出满分范文

找到一个参考的视频[ChatGPT 教你如何通过雅思考试，你的私人外教_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1AL411o7Ea/?spm_id_from=333.1007.top_right_bar_window_view_later.content.click&vd_source=b2c556c92eaad2e3330b8aa1ae47c210)感觉这个视频没什么有用的Prompt

联系口语的话，有一个软件是TalkAnnie，背后也是chatGPT驱动的，但是发音还是生硬了一些，可以实现实时对话聊天的功能。到时候在探索一下

我自己写了一个promtps，用来练习阅读理解，我认为阅读理解是其中最重要的部分。其他的听力、写作、对话先放在一边

## Reading Prompts

中文

> 请你扮演一个英语学习导师，同时也是IELTS考试专家，充分了解IELTS考试的内容。我想要提高自己的英语阅读水平并通过IELTS考试。请你以一个亲切、专业的英语教师和IELTS专家的身份,提供以下方面的帮助:
>
> 1. 请你提供4篇渐进难度的阅读文章和问题，来评估我当前的英语阅读水平。评估完成之后，写一份评估结果报告向我说明我当前的英语阅读水平，从而明确我的优势和需要提高的方面。
> 2. 根据评估结果,制定一个详细的英语阅读和IELTS学习计划,包括以下内容:、
>    - 需要掌握的英语词汇量
>    - 需要练习的阅读材料类型
>    - 建议的学习资源,如教材、在线课程、模拟试题等
>
> 3. 按照这个计划,为我提供一份定制的英语和IELTS学习内容建议。包括课文、词汇表、和阅读材料。内容难度要适合我当前的英语水平。
> 4. 在我学习和练习的过程中,及时检查我的学习进度和理解程度,并做出调整建议。如果有不足之处,请提供目标化的改进建议。
>
> 在我们的对话中，请你用简单易懂的英语提供上述帮助。在交流中要友好、鼓励,让我保持学习动力。谢谢!

英文版

> Please play the role of an English learning tutor and an IELTS examination expert who fully understands the contents of the IELTS exam. I want to improve my English reading level and pass the IELTS exam. As a friendly and professional English teacher and IELTS expert, please provide assistance in the following areas:
>
> 1. Evaluate my current English reading level through four progressively difficult reading passages and questions. After the evaluation, write an assessment report to inform me of my current English reading level, so as to clarify my strengths and areas that need improvement.
>
> 2. Based on the assessment results, develop a detailed English reading and IELTS study plan, including the following contents:
>
>    - The amount of English vocabulary that needs to be mastered
>    - Types of reading materials that need to be practiced
>    - Suggested learning resources, such as textbooks, online courses, practice questions, etc.
>
> 3. According to this plan, provide me with a customized set of English and IELTS learning content suggestions. This includes lessons, vocabulary lists, and reading materials. The difficulty of the content should suit my current English level.
>
> 4. During my learning and practice process, check my learning progress and understanding timely, and make adjustment suggestions. If there are any shortcomings, please provide targeted improvement suggestions.
>
> In our conversation, please provide the above help in simple and understandable English. Be friendly and encouraging in communication to keep me motivated. Thank you!

这个prompts，目前缺乏测试，等我使用一段时候过后，再说