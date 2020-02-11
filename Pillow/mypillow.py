#-*- coding: utf-8 -*-
import math
import operator

from PIL import Image, ImageChops
import os
import logging
class mypillow:
    def compare_images(self,img1):

        img2 = img1.replace('Result','Expect')#预期结果的路径
        img3 = img1.replace('Result', 'Diff')#对比结果图存放的位置

        with Image.open(r"%s" % (img1.encode('gbk'))) as img_exp, Image.open(r"%s" % (img2.encode('gbk'))) as img_rel:
            exp = img_exp.histogram()
            expect_width, expect_height = img_exp_size = img_exp.size
            rel = img_rel.histogram()
            result_width, result_height = img_rel_size = img_rel.size
            if len(exp) != len(rel):
                logging.info("图片不一致！")
                return False
            else:
                result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, exp, rel))) / len(exp))
                if result < 1:
                    return True
                else:
                    if img_exp_size == img_rel_size:
                        pass
                    else:
                        # 预期图片的尺寸更大
                        if img_rel_size < img_exp_size:
                            box = (0, 0, result_width, result_height)
                            # print box
                            img_exp.crop(box).save(img1.encode('gbk'))
                            # print 'change expect picture dimension'
                        # 结果图片的尺寸更大
                        else:
                            box = (0, 0, expect_width, expect_height)
                            # print box
                            img_rel.crop(box).save(img2.encode('gbk'))
                            # print 'change result picture dimension'
                    # result_width, result_height = img_rel_size = img_rel.size
                    diff = ImageChops.difference(img_exp, img_rel)
                    diff_pix = diff.getbbox()
                    h = diff.histogram()
                    sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
                    sum_of_squares = sum(sq)
                    rms = math.sqrt(sum_of_squares / float(img_exp.size[0] * img_rel.size[1]))  # root mean square均方根
                    if diff_pix is None:
                        return True
                    else:
                        # 加载两张图片并将他们转换为灰度
                        import cv2
                        from skimage.measure import compare_ssim
                        import imutils
                        image_expect_picture = cv2.imread(r"%s" % (img1.encode('gbk')))
                        image_result_picture = cv2.imread(r"%s" % (img2.encode('gbk')))
                        gray_expect_picture = cv2.imread(r"%s" % (img1.encode('gbk')), 0)
                        gray_result_picture = cv2.imread(r"%s" % (img2.encode('gbk')), 0)
                        # 计算两个灰度图像之间的结构相似度指数
                        (score, diff) = compare_ssim(gray_expect_picture, gray_result_picture, full=True)
                        diff = (diff * 255).astype("uint8")
                        # 找到不同点的轮廓以致于我们可以在被标识为“不同”的区域周围放置矩形
                        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                        # 找到一系列区域，在区域周围放置矩形
                        for c in cnts:
                            (x, y, w, h) = cv2.boundingRect(c)
                            cv2.rectangle(image_expect_picture, (x, y), (x + w, y + h), (0, 0, 255), 2)
                            cv2.rectangle(image_result_picture, (x, y), (x + w, y + h), (0, 0, 255), 2)

                        # 用cv2.imshow展现最终对比之后的图片， cv2.imwrite保存最终的结果图片
                        cv2.imshow("Modified", image_result_picture)
                        cv2.imwrite(img3.encode("gbk"), image_result_picture)
                        cv2.destroyAllWindows()
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return False
if __name__ == '__main__':
    print("ok")

    currentPath=os.path.dirname(os.path.abspath(__file__))
    print(currentPath)
    imgPath=os.path.join(currentPath+"\img\Result\historyApprover.png")
    # print(imgPath)
    # im=Image.open(imgPath)
    # print(im.size)
    # print(im.histogram())
    mp=mypillow()
    # mp.compare_images(imgPath)
    mp.compare_images(imgPath)