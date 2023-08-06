这是做什么的？
=======================
这是一个图像模板识别替换工具，根据提供的模板识别目标图像是否包含指定的logo或水印（或其他的图像模式），
可设置自动完成替换或渐变填充并保存或返回图像二进制流

怎么安装？
=======================
  pip install imrepltool


怎么使用
=======================

导入并实例化：


  from imrepltool.imrepltool import ImreplTool

  IT = ImreplTool(cover_up=False,
                  cover_with_img=False,
                  cover_color=None,
                  log_level=None,
                  optimize_t_sequence=True)


在实例化时有数个选项可提供设置：
 - cover_up                为bool值，设置是否覆盖图像被匹配的地方，设置后对于处理速度有一定影响；
 - cover_with_img          为bool值，设置是否使用您自己的logo或水印来覆盖被匹配的区域；
 - cover_color             为颜色rgb值（列表: [0, 156, 255]）， 注意，当 cover_with_img 为True 时此项无效；
 - log_level               为日志级别，需要使用python 内置logging 包进行设置，例如： logging.ERROR， 默认是 logging.INFO 级别
 - optimize_t_sequence     为bool值， 设置是否在程序退出前对模板数据库排列进行优化，以提升下次运行速度


若您只是想检查目标图像是否包含已知模板，则不需要设置以上选项，直接默认实例化即可:

  IT = ImreplTool()

在第一次安装使用时，您需要导入模板数据:


  template_paths = [
      ['SJZG', 'templates/shijuezhongguo_template_1.jpg', 81],    # 这样的格式是必须的
      ['SJZG', 'templates/shijuezhongguo_template_4.jpg', 0],]

  IT.add_templates(templates=template_paths, update_if_existed=False)   # update_if_existed 若已存在则更新


template_paths 需要一个二维列表， 内部的每一条即为一个模板记录，每条记录需要三个数据：
 - 0 ： 模板名称（即上面的 SJZG 对应的位置）
 - 1 ： 模板位置，可以是本地相对路径或绝对路径，也可以是图片网址（即上面的 .jpg 对应的位置）
 - 2 ： 模板阈值，在匹配模板时阈值越高越精确，但也可能导致匹配不上，若不确定多少值，则设置为 0 即可（即上面的 81 对应的位置）


若在初始化时设置了 cover_with_img=True，则还需要导入替换 logo 的信息：

  replacements = [
      ['SJZG', 'replacement/611_logo.png'],]

  IT.add_replace_img(repl_paths=replacements)


与 template_paths 一样，需要一个二维列表， 但是每条记录只需要两个数据：
 - 0： logo对应的模板名称，即您希望此logo替换哪一个模板，注意此名称需要和 template_paths 的模板名称一致
 - 1： logo位置，可以是本地相对路径或绝对路径，也可以是图片网址

图像数据输入完毕，接下来进行初始化就可以使用了：

  IT.initialize_data(template_names='SJZG')

初始化时可以指明使用哪一个模板进行识别，即 template_names，若有多个模板需要使用，则使用列表将模板名称包装起来：

  IT.initialize_data(template_names=['SJZG', 'other1', 'other2', ...])


若您需要对图像有选择性的覆盖，则在设置了 cover_with_img=True 和导入替换logo信息后，还可以设置：

  IT.COVER_TEMPLATES = ['SJZG']

即可指明程序覆盖哪一类模板，若不设置则自动覆盖所有匹配到的模板

接下来可以正式使用匹配程序了：

  image = 'images/shijuezhongguo_1.jpg'

  # image = "http://chuantu.xyz/t6/702/1565924123x2890171859.jpg"  # 或者图片的网址

  check_result = IT.check(image)

需要注意的是，check 函数只接收单个图像地址， 若需要处理多张图片，请在初始化后使用循环条件调用 check

返回的 check_result 如下：

  {'SJZG': True}

  # {'SJZG': False}   # 若匹配不上则为 False

此外若有需要，您还可以使用 score = IT.FINAL_SCORE 来查看对应的匹配分数，score的值为：

  {'SJZG': 0.9999}

如果您想检查图像覆盖情况，则可以使用：

  IT.show()

将显示处理后的图像，但是需要注意的是，若您有多个图像在循环处理，您需要手动关闭显示的图像才能继续运行，每次显示一张图片

然后您可以保存处理后的图像：

  save_result = IT.save('replaced_image.jpg')

如果您给定了保存地址，则保存成功后 save_result 的值为 True（保存失败则返回 False ），

若没有给定保存地址，则 save_result 的值为处理后的图像的二进制流，您可以使用其他工具将其保存或者上传到网站


到此程序流程完成

其他选项
========
其他的图像覆盖设置为可选项，若您有兴趣，或者发现覆盖效果不理想的时候，可以尝试调整这些选项查看效果

  IT.EP_METHOD = False                # encircling picking method 是否启用三点包围取点法， False 则启用直线取点法

  IT.EP_DISTANCE = 3                  # 三点包围取点法的像素取点距离

  IT.SP_PIX = 3                       # straight picking method 直线取点法的像素取点数

  IT.BORDER_EXTEND = 8                # 匹配边界的覆盖扩展像素数

  IT.KEEP_COVER_IMG_SCALE = True      # 填充logo是否保持原比例

  IT.CONCENTRATION = 100              # 填充透明度（尚不完善）
