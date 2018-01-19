# pytorch-lambdapack

For complete explanation, refer to [the blog post](https://dreamgonfly.github.io/2018/01/20/pytorch-on-aws-lambda.html)

##  To build lambdapack

```shell
sh build_pack.sh
```

## To add to lambdapack

If you already built a lambdapack, you don't need to build the whole pack again when you changed files. Just run the below command and it adds the files to the pack.

```shell
sh add_pack.sh
```

## To test locally

Change the environment variables and test event in `local_test.py` to fit your case, then you can test your lambda function locally.

```shell
sh local_test.sh
```

